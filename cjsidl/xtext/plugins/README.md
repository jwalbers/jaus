# Using the CJSIDL Editor for .jaus files

The jar files in this directory were produced for some short-notice collaboration.  When and if we have a maintainable release, these will be packaged as an Eclipse site archive.

This 1.0.0.BETA CJSIDL editor plugin is built with and for a neon-3 platform. The plugin uses the Xtext file in this repository, using the standard Xtext project setup.

For now, install in the dropins folder.

1. Shutdown your eclipse application.
1. Download the three jar files that make up the editor plugin.
   * com.fastpilot.jaus.cjsidl.ide_1.0.0.BETA.jar
   * com.fastpilot.jaus.cjsidl.ui_1.0.0.BETA.jar
   * com.fastpilot.jaus.cjsidl_1.0.0.BETA.jar
1. In your eclipse installation, you will find a ‘dropins’ directory.
1. If ‘dropins’ does not already have a ‘plugins’ directory, create one.
1. Copy the three jar files into the ‘plugins’ directory.
1. Restart the eclipse application with the ‘-clean’ argument to clear the plugins cache and load the new ‘dropins’ plugins.
1. Create a new workspace
1. Create a new General Project
1.  Create a new file “sample.jaus’
1. The file will automatically open in the “Jaus Editor”. To confirm the CJSIDL editor plugin is installed, you can right click on the sample.jaus file in the project explorer, select “Open with...” and note that “Jaus Editor” is one of the options.
1. Paste in CJSIDL contents and save the file.   Note errors detected by the editor’s CJSIDL parser.  If you use the test case file 5710A_Transport.jaus there are two errors in the ‘protocol’ section, with useful error messages when you float over the “X” markers.

## Known issues

* Content assist (CTRL-SPACE) does not have 100% coverage, not sure why. There are a few cases in parameter lists where it does not appear to suggest the right keyword args.
* The Outline view could be prettier.  See the Dr. Dobbs article for a good how-to tutorial that highlights Xtext extensibility. [http://www.drdobbs.com/architecture-and-design/customizing-xtext/231902091]

 
