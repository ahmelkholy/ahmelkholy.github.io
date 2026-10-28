# Copy public, prebuilt documentation after Jekyll; never run it through Liquid.
require "fileutils"
Jekyll::Hooks.register :site, :post_write do |site|
  source = File.join(site.source, "static-docs")
  next unless Dir.exist?(source)
  Dir.children(source).sort.each do |name|
    raise "Invalid static docs project: #{name}" unless name.match?(/\A[a-z0-9][a-z0-9-]*\z/)
    project = File.join(source, name)
    raise "Expected docs directory: #{name}" unless File.directory?(project) && !File.symlink?(project)
    raise "Missing static docs index: #{name}" unless File.file?(File.join(project, "index.html"))
    # Source collision check works on repeated incremental serve rebuilds too.
    raise "Native/imported docs collision: #{name}" if File.exist?(File.join(site.source, "docs", name))
    Dir.glob(File.join(project, "**", "*"), File::FNM_DOTMATCH).each do |entry|
      next if [".", ".."].include?(File.basename(entry))
      raise "Symlink or hidden file in imported docs: #{entry}" if File.symlink?(entry) || File.basename(entry).start_with?(".")
    end
    target = File.join(site.dest, "docs", name)
    FileUtils.mkdir_p(File.dirname(target))
    FileUtils.rm_rf(target)
    FileUtils.cp_r(project, target)
  end
end
