# frozen_string_literal: true

# A post and its figures can live together under _posts/<topic>/. Register only
# assets that a published post actually references; Jekyll then copies and cleans
# them like ordinary static files. The Markdown source stays portable and intact.
require "cgi"
require "pathname"
require "uri"

module PostAssets
  EXTENSIONS = %w[.svg .png .jpg .jpeg .gif .webp .avif .ico .tif .tiff .pdf].freeze
  ATTRIBUTES = {
    "a" => %w[href], "img" => %w[src srcset], "source" => %w[src srcset],
    "video" => %w[poster], "object" => %w[data]
  }.freeze
  # Keep comments and raw-text elements opaque. Match quoted '>' characters as
  # part of a tag, and change only the selected URL attribute, not other markup.
  TOKENS = %r{<!--.*?-->|<(script|style|textarea)\b[^>]*>.*?</\1\s*>|<[a-z][a-z0-9:-]*\b(?:[^>"']|"[^"]*"|'[^']*')*>}im.freeze
  ATTRIBUTE = /(?<space>\s+)(?<name>[a-z_:][a-z0-9_.:-]*)(?<equals>\s*=\s*)(?:"(?<double>[^"]*)"|'(?<single>[^']*)'|(?<bare>[^\s>]+))/i.freeze

  class Asset < Jekyll::StaticFile
    def initialize(site, relative_source, public_url)
      super(site, site.source, File.dirname(relative_source), File.basename(relative_source))
      @public_url = public_url
    end

    def url
      @public_url
    end

    def destination_rel_dir
      Jekyll::URL.unescape_path(File.dirname(url))
    end
  end

  class Resolver
    def initialize(post)
      @post = post
      @site = post.site
      @posts_root = File.expand_path("_posts", @site.source)
      @source = File.expand_path(post.path, @site.source)
    end

    def rewrite(html)
      return html unless within?(@source, @posts_root)

      html.gsub(TOKENS) do |tag|
        name = tag[/\A<([a-z][a-z0-9:-]*)\b/i, 1]&.downcase
        allowed = ATTRIBUTES[name]
        next tag unless allowed

        tag.gsub(ATTRIBUTE) do |attribute|
          match = Regexp.last_match
          next attribute unless allowed.include?(match[:name].downcase)

          value = match[:double] || match[:single] || match[:bare]
          decoded = CGI.unescapeHTML(value)
          rewritten = if match[:name].downcase == "srcset"
                        rewrite_srcset(decoded)
                      else
                        resolve(decoded)
                      end
          next attribute if rewritten == decoded

          # Always quote a rewritten URL, including an originally unquoted one.
          "#{match[:space]}#{match[:name]}#{match[:equals]}\"#{CGI.escapeHTML(rewritten)}\""
        end
      end
    end

    private

    def rewrite_srcset(value)
      # A data URI contains commas; leave that mixed/raw form untouched. Ordinary
      # local srcset candidates use URL-encoded spaces and standard descriptors.
      return value if value.match?(/(?:\A|\s)data:/i)

      value.split(",", -1).map do |candidate|
        candidate.sub(/\S+/) { |url| resolve(url) }
      end.join(",")
    end

    def resolve(url)
      return url if url.empty? || url.start_with?("/", "#") || url.match?(/\A[a-z][a-z0-9+.-]*:/i)

      encoded_path, suffix = url.split(/(?=[?#])/, 2)
      path = URI::DEFAULT_PARSER.unescape(encoded_path)
      return url unless EXTENSIONS.include?(File.extname(path).downcase)

      source = File.expand_path(path, File.dirname(@source))
      # Existing website-relative links outside _posts are left to Jekyll and the
      # site's link checker. This plugin only owns bundled post assets.
      return url unless within?(source, @posts_root)

      relative = Pathname.new(source).relative_path_from(Pathname.new(@posts_root)).to_s
      fail_asset(url, "hidden files cannot be published") if relative.split("/").any? { |part| part.start_with?(".") }
      parts = relative.split("/")
      cursor = @posts_root
      parts.each do |part|
        cursor = File.join(cursor, part)
        fail_asset(url, "symlinks cannot be published") if File.symlink?(cursor)
      end
      fail_asset(url, "file does not exist; check its name and path relative to this Markdown file") unless File.file?(source)

      public_url = "/assets/posts/#{URI::DEFAULT_PARSER.escape(relative, /[^A-Za-z0-9\-._~\/]/)}"
      relative_source = Pathname.new(source).relative_path_from(Pathname.new(@site.source)).to_s
      asset = Asset.new(@site, relative_source, public_url)
      target = asset.destination(@site.dest)
      existing = @site.static_files.find { |item| item.destination(@site.dest) == target }
      if existing
        fail_asset(url, "output conflicts with #{existing.relative_path}") unless File.expand_path(existing.path) == source
      else
        fail_asset(url, "output conflicts with a page or post") if @site.pages.any? { |page| page.destination(@site.dest) == target } || @site.documents.any? { |doc| doc.destination(@site.dest) == target }
        @site.static_files << asset
      end

      "#{@site.baseurl.to_s.sub(%r{/\z}, '')}#{public_url}#{suffix}"
    end

    def within?(path, directory)
      path.start_with?("#{directory}/")
    end

    def fail_asset(url, reason)
      raise Jekyll::Errors::FatalException, "Post asset error in #{@post.relative_path}: #{url.inspect}: #{reason}."
    end
  end
end

Jekyll::Hooks.register :posts, :post_convert do |post|
  resolver = PostAssets::Resolver.new(post)
  post.content = resolver.rewrite(post.content)
  # Excerpts have their own renderer and do not fire document hooks. Normalize
  # them too so images work in indexes, feeds and future excerpt-based layouts.
  excerpt = post.data["excerpt"]
  excerpt.output = resolver.rewrite(excerpt.output) if excerpt.is_a?(Jekyll::Excerpt)
end
