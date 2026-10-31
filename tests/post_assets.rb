# frozen_string_literal: true

# Build tiny isolated sites so no fixture ever becomes a real public article.
# Run with: bundle exec ruby tests/post_assets.rb
require "jekyll"
require "tmpdir"
require "fileutils"

root = File.expand_path("..", __dir__)

def write_file(root, path, content)
  target = File.join(root, path)
  FileUtils.mkdir_p(File.dirname(target))
  File.write(target, content)
end

def check(condition, message)
  raise message unless condition
end

Dir.mktmpdir("jekyll-post-assets-") do |temporary|
  source = File.join(temporary, "source")
  destination = File.join(temporary, "output")
  FileUtils.mkdir_p(File.join(source, "_plugins"))
  FileUtils.cp(File.join(root, "_plugins/post_assets.rb"), File.join(source, "_plugins/post_assets.rb"))
  write_file(source, "index.html", "---\n---\n{% for post in site.posts %}<a href=\"{{ post.url | relative_url }}\">{{ post.title }}</a>{{ post.excerpt }}{% endfor %}")
  write_file(source, "feed.xml", "---\n---\n<feed>{% for post in site.posts %}<entry>{{ post.content | xml_escape }}</entry>{% endfor %}</feed>")
  alpha = <<~POST
    ---
    title: Alpha
    permalink: /custom/alpha/
    ---
    ![Alpha](figs/shared.svg?version=1&mode=full#diagram)

    <figure><img src='figs/space%20name.svg' alt="Space > name"><figcaption>Paper source.</figcaption></figure>
    ![Spaced directory](figs/space%20directory/diagram.svg)
    <img src=figs/shared.svg alt="Unquoted">
    <img src="figs/shared.svg" srcset="figs/shared.svg 1x, figs/space%20name.svg 2x" alt="Responsive">
    [Download paper](figs/paper.pdf#page=2)
    ![External](https://example.test/remote.svg)
    ![Root](/images/shared.svg)
    <a href="#local">Anchor</a>
    <span id="local">Target</span>
    <!-- <img src="figs/comment-only.svg"> -->
    <script>const example = '<img src="figs/script-only.svg">';</script>

    ```html
    <img src="figs/code-only.svg">
    ```
  POST
  write_file(source, "_posts/alpha/2020-01-02-alpha.md", alpha)
  write_file(source, "_posts/alpha/figs/shared.svg", '<svg xmlns="http://www.w3.org/2000/svg"><title>Alpha bytes</title></svg>')
  write_file(source, "_posts/alpha/figs/space name.svg", '<svg xmlns="http://www.w3.org/2000/svg"><title>Space bytes</title></svg>')
  write_file(source, "_posts/alpha/figs/space directory/diagram.svg", '<svg xmlns="http://www.w3.org/2000/svg"><title>Directory bytes</title></svg>')
  write_file(source, "_posts/alpha/figs/paper.pdf", "%PDF-1.4\nfixture\n")
  write_file(source, "_posts/alpha/figs/unreferenced.svg", "DO_NOT_COPY")
  write_file(source, "_posts/beta/2020-01-03-beta.md", "---\ntitle: Beta\n---\n![Beta](figs/shared.svg)\n")
  write_file(source, "_posts/beta/figs/shared.svg", '<svg xmlns="http://www.w3.org/2000/svg"><title>Beta bytes</title></svg>')
  write_file(source, "_posts/2020-01-04-flat.md", "---\ntitle: Flat\n---\n![Legacy](flat/old.svg)\n![Bundle](flat/figs/new.svg)\n")
  write_file(source, "_posts/flat/old.svg", "LEGACY_ASSET")
  write_file(source, "_posts/flat/figs/new.svg", "FLAT_BUNDLE_ASSET")
  write_file(source, "_posts/hidden/2020-01-01-hidden.md", "---\ntitle: Hidden\npublished: false\n---\n![Never](figs/missing.svg)\n")
  write_file(source, "_posts/hidden/figs/private.svg", "HIDDEN_ASSET")
  write_file(source, "_posts/future/2099-01-01-future.md", "---\ntitle: Future\n---\n![Never](figs/missing.svg)\n")
  write_file(source, "_drafts/draft.md", "---\ntitle: Draft\n---\n![Never](figs/missing.svg)\n")
  config = Jekyll.configuration(
    "source" => source, "destination" => destination, "quiet" => true,
    "baseurl" => "/preview", "url" => "https://example.test",
    "permalink" => "/articles/:year/:month/:title/", "future" => false,
    "disable_disk_cache" => true
  )
  site = Jekyll::Site.new(config)
  site.process

  html = File.read(File.join(destination, "custom/alpha/index.html"))
  check(html.include?('/preview/assets/posts/alpha/figs/shared.svg?version=1&amp;mode=full#diagram'), "query/fragment or baseurl lost")
  check(html.include?('/preview/assets/posts/alpha/figs/space%20name.svg'), "percent-encoded filename failed")
  check(html.include?('/preview/assets/posts/alpha/figs/space%20directory/diagram.svg'), "percent-encoded directory failed")
  check(html.include?('src="/preview/assets/posts/alpha/figs/shared.svg"'), "unquoted/raw HTML image failed")
  check(html.include?('srcset="/preview/assets/posts/alpha/figs/shared.svg 1x, /preview/assets/posts/alpha/figs/space%20name.svg 2x"'), "srcset failed")
  check(html.include?('href="/preview/assets/posts/alpha/figs/paper.pdf#page=2"'), "relative PDF link failed")
  check(html.include?('https://example.test/remote.svg') && html.include?('src="/images/shared.svg"') && html.include?('href="#local"'), "external/root/anchor URL changed")
  check(html.include?('src="figs/comment-only.svg"') && html.include?('src="figs/script-only.svg"') && html.include?('figs/code-only.svg'), "comment/script/code changed")
  %w[alpha/figs/shared.svg alpha/figs/space\ name.svg alpha/figs/space\ directory/diagram.svg alpha/figs/paper.pdf beta/figs/shared.svg flat/old.svg flat/figs/new.svg].each do |path|
    check(File.binread(File.join(source, "_posts", path)) == File.binread(File.join(destination, "assets/posts", path)), "asset bytes changed: #{path}")
  end
  check(!File.exist?(File.join(destination, "assets/posts/alpha/figs/space%20directory")), "URL escaping leaked into the filesystem directory")
  check(!File.exist?(File.join(destination, "assets/posts/alpha/figs/unreferenced.svg")), "unreferenced asset published")
  check(!File.exist?(File.join(destination, "assets/posts/hidden")), "hidden asset published")
  check(!File.exist?(File.join(destination, "_posts")), "source post directory published")
  index = File.read(File.join(destination, "index.html"))
  check(index.include?('href="/preview/custom/alpha/"') && index.include?("Beta") && index.include?("Flat"), "new posts missing from index")
  check(index.include?('/preview/assets/posts/alpha/figs/shared.svg'), "excerpt image URL failed")
  check(!index.match?(/Hidden|Future|Draft/), "draft/future article published")
  check(File.read(File.join(destination, "feed.xml")).include?('/preview/assets/posts/alpha/figs/shared.svg'), "feed image URL failed")
  check(File.read(File.join(source, "_posts/alpha/2020-01-02-alpha.md")) == alpha, "Markdown source was modified")

  # A regular rebuild removes an asset that is no longer referenced.
  write_file(source, "_posts/alpha/2020-01-02-alpha.md", "---\ntitle: Alpha\npermalink: /custom/alpha/\n---\nNo more figures.\n")
  site.process
  check(!File.exist?(File.join(destination, "assets/posts/alpha")), "obsolete bundled assets survived a rebuild")

  # Missing assets fail with the document and URL, before anything is deployed.
  write_file(source, "_posts/alpha/2020-01-02-alpha.md", "---\ntitle: Alpha\n---\n![Missing](figs/missing.svg)\n")
  begin
    site.process
    raise "missing figure unexpectedly built"
  rescue Jekyll::Errors::FatalException => error
    check(error.message.include?("_posts/alpha/2020-01-02-alpha.md") && error.message.include?("figs/missing.svg") && error.message.include?("file does not exist"), "missing-asset error was not actionable")
  end
end

puts "PASS: nested/flat bundles, automatic indexes, original asset bytes, baseurl/custom permalink, HTML/srcset/PDF URLs, excerpts/feed, draft/future exclusion, cleanup and missing-figure errors."
