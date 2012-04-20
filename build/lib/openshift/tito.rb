require 'fileutils'

DEVENV_REGEX = /^rhc-devenv-\d+/
SIBLING_REPOS = [['crankcase', '../crankcase'],
                 ['crankcase', '/var/lib/jenkins/jobs/crankcase/workspace'],
                 ['os-client-tools', '../os-client-tools'],
                 ['os-client-tools', '/var/lib/jenkins/jobs/os-client-tools/workspace']]
  
PACKAGE_REGEX = /^([\w-]*)-\d+\.\d+\.\d+-\d+\.\..*:$/
IGNORE_PACKAGES = ['stickshift-broker']

module OpenShift
  module Tito

    def get_build_dirs
      # Figure out what needs to be built
      packages = `tito report --untagged-commits`
      all_packages = get_packages
      build_dirs = []
      packages.split("\n").collect do |package|
        if package =~ PACKAGE_REGEX
          pkg = $1
          #unless IGNORE_PACKAGES.include?(pkg)
            build_dirs << [pkg, all_packages[pkg][0], all_packages[pkg][1]]
          #end
        end
      end
      SIBLING_REPOS.each do |repo_info|
        repo_name = repo_info[0]
        repo_dir = repo_info[1]
        if File.exists?(repo_dir)
          packages = `cd #{repo_dir} && tito report --untagged-commits`
          packages.split("\n").collect do |package|
            if package =~ PACKAGE_REGEX
              pkg = $1
              #unless IGNORE_PACKAGES.include?(pkg)
                build_dirs << [pkg, all_packages[pkg][0], all_packages[pkg][1]]
              #end
            end
          end
        end
      end
      build_dirs
    end

    def get_sync_dirs
      # Figure out what needs to be synced
      tito_report = `tito report --untagged-commits`
      current_package = nil
      FileUtils.mkdir_p "/tmp/devenv/sync/"
      current_package_contents = ''
      current_package = nil
      current_sync_dir = nil
      sync_dirs = []
      packages = tito_report.split("\n")
      all_packages = get_packages
      packages.each do |package|
        if package =~ DEVENV_REGEX
          puts "The devenv package has an update but isn't being installed."
        elsif package =~ PACKAGE_REGEX
          pkg = $1
          unless IGNORE_PACKAGES.include?(pkg)
            current_package = pkg
            current_sync_dir = all_packages[current_package][0]
          end
        elsif package =~ /---------------------/
          if current_package
            update_sync_history(current_package, current_package_contents, current_sync_dir, sync_dirs)
            current_package_contents = ''
            current_package = nil
            current_sync_dir = nil
          end
        end
        current_package_contents += package if current_package
      end
      update_sync_history(current_package, current_package_contents, current_sync_dir, sync_dirs) if current_package
      current_package_contents = ''
      current_package = nil
      current_sync_dir = nil
      sync_dirs.compact!
      SIBLING_REPOS.each do |repo_info|
        repo_name = repo_info[0]
        repo_dir = repo_info[1]
        if File.exists?(repo_dir)
          packages = `cd #{repo_dir} && tito report --untagged-commits`
          packages.split("\n").collect do |package|
            if package =~ PACKAGE_REGEX
              pkg = $1
              unless IGNORE_PACKAGES.include?(pkg)
                current_package = pkg
                current_sync_dir = all_packages[pkg][0]
              end
            end
            current_package_contents += package if current_sync_dir
          end
          update_sync_history(current_package, current_package_contents, current_sync_dir, sync_dirs) if current_package
          sync_dirs.compact!
        end
      end
      sync_dirs
    end

    def get_stale_dirs
      stale_dirs = []
      packages = get_packages
      packages.each do |package_name, build_info|
        unless IGNORE_PACKAGES.include?(package_name)
          build_dir = build_info[0]
          spec_file = build_info[1]
          installed_version = `yum list installed #{package_name} | tail -n1 | gawk '{print $2}'`
          if installed_version =~ /(\d+\.\d+\.\d+)-/
            installed_version = $1
            spec_version = /Version: *(.*)/.match(File.read(spec_file))[1].strip
            installed_version_parts = installed_version.split(".").map { |part| part.to_i }
            spec_version_parts = spec_version.split(".").map { |part| part.to_i }
            stale_dirs << [package_name, build_dir] if (installed_version_parts <=> spec_version_parts) < 0
          end
        end
      end
      stale_dirs
    end

    def get_packages
      packages = {}
      dirs = ['.']
      SIBLING_REPOS.each do |repo_info|
        repo_name = repo_info[0]
        repo_dir = repo_info[1]
        if File.exists?(repo_dir)
          dirs << repo_dir
        end
      end
      dirs.each do |repo_dir|
        Dir.glob("#{repo_dir}/**/*.spec") do |file|
          unless file.start_with?('build/')
            build_dir = File.dirname(file)
            package_name = /Name: *(.*)/.match(File.read(file))[1].strip
            while (package_name =~ /%\{([^\{\}]*)\}/)
              var_name = $1
              var_val = /%global *#{var_name} *(.*)/.match(File.read(file))[1].strip
              package_name.gsub!("%{#{var_name}}", var_val)
            end
            packages[package_name] = [build_dir, file]
          end
        end
      end
      packages
    end

    def update_sync_history(current_package, current_package_contents, current_sync_dir, sync_dirs)
      current_package_file = "/tmp/devenv/sync/#{current_package}"
      previous_package_contents = nil
      if File.exists? current_package_file
        previous_package_contents = `cat #{current_package_file}`.chomp
      end
      unless previous_package_contents == current_package_contents
        sync_dirs << [current_package, current_sync_dir]
        file = File.open(current_package_file, 'w')
        begin
          file.print current_package_contents
        ensure
          file.close
        end
      else
        puts "Latest package already installed for: #{current_package}"
      end
    end
  end
end
