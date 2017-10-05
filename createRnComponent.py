import sublime, sublime_plugin
import functools
import os

def Window(window = None):
  return window if window else sublime.active_window()

class SidebarNewRnComponentCommand(sublime_plugin.WindowCommand):
  def run(self, paths = [], name = ""):
    Window().run_command('hide_panel');
    Window().show_input_panel("(Native) Component Name:", "", functools.partial(self.on_done, paths, False), None, None)

  def on_done(self, paths, relative_to_project, name):
    path = paths[len(paths) - 1] + '/' + name
    if os.path.exists(path):
      sublime.error_message("Unable to create folder, folder or file exists.")
      return

    os.makedirs(path)

    componentFilePath = path + '/' + name + '.js'
    componentStr = """import React from 'react';
import {{ View, Text }} from 'react-native';
import styles from './{0}.styles';

export default class {0} extends React.Component {{
  render() {{
    return (
      <View>
        <Text>{0}</Text>
      </View>
    );
  }}
}}
""".format(name)

    with open(componentFilePath, 'w+', encoding='utf8', newline='') as f:
      f.write(componentStr)

    indexFilePath = path + '/index.js'
    with open(indexFilePath, 'w+', encoding='utf8', newline='') as f:
      f.write("export {{ default }} from './{0}';\n".format(name))

    styleFilePath = path + '/' + name + '.styles.js'
    styleStr = """import { StyleSheet } from 'react-native';

export default StyleSheet.create({

});
"""
    with open(styleFilePath, 'w+', encoding='utf8', newline='') as f:
      f.write(str(styleStr))

class SidebarNewRwComponentCommand(sublime_plugin.WindowCommand):
  def run(self, paths = [], name = ""):
    Window().run_command('hide_panel');
    Window().show_input_panel("(Web) Component Name:", "", functools.partial(self.on_done, paths, False), None, None)

  def on_done(self, paths, relative_to_project, name):
    path = paths[len(paths) - 1] + '/' + name
    if os.path.exists(path):
      sublime.error_message("Unable to create folder, folder or file exists.")
      return

    os.makedirs(path)

    componentFilePath = path + '/' + name + '.js'
    componentStr = """import React from 'react';
import styles from './{0}.css';

export default class {0} extends React.Component {{
  render() {{
    return (
      <div className={{styles.container}}>
        {0}
      </div>
    );
  }}
}}
""".format(name)

    with open(componentFilePath, 'w+', encoding='utf8', newline='') as f:
      f.write(componentStr)

    indexFilePath = path + '/index.js'
    with open(indexFilePath, 'w+', encoding='utf8', newline='') as f:
      f.write("export {{ default }} from './{0}';\n".format(name))

    styleFilePath = path + '/' + name + '.css'
    styleStr = """.container {}"""
    with open(styleFilePath, 'w+', encoding='utf8', newline='') as f:
      f.write(str(styleStr))
