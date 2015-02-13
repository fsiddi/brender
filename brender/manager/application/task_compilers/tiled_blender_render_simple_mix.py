import os
import json
import logging

from application import app

class task_compiler():
    @staticmethod
    def compile(worker, task):

      settings=json.loads(task['settings'])

      if 'Darwin' in worker.system:
         setting_blender_path = app.config['BLENDER_PATH_OSX']
         setting_render_settings = app.config['SETTINGS_PATH_OSX']
         file_path = settings['file_path_osx']
         output_path = settings['output_path_osx']
      elif 'Windows' in worker.system:
         setting_blender_path = app.config['BLENDER_PATH_WIN']
         setting_render_settings = app.config['SETTINGS_PATH_WIN']
         file_path = settings['file_path_win']
         output_path = settings['output_path_win']
      else:
         setting_blender_path = app.config['BLENDER_PATH_LINUX']
         setting_render_settings = app.config['SETTINGS_PATH_LINUX']
         file_path = settings['file_path_linux']
         output_path = settings['output_path_linux']

      blender_path = setting_blender_path

      if setting_render_settings is None:
         logging.warning("Render settings path not set!")

      #tile_output_path="{0}_{1}".format(output_path, settings['tile'])
      tile_output_path="{0}/".format(output_path)

      render_settings = os.path.join(
         setting_render_settings,
          settings['render_settings'])

      #render_folder=os.path.split(tile_output_path)[0]

      for tile in range(0, settings['tiles']):
        script_path=os.path.join(output_path , 'tile_mix')

        dir = os.path.dirname(__file__)
        template_path = os.path.join(dir, 'tiled_blender_render_simple_mix.template')
        with open (template_path, "r") as f:
          script=f.read()
        f.close()

        data="""
tiles={0}
output='{1}'
frame={2}
      """.format(settings['tiles'], os.path.join(output_path, 'tiled'), settings['frame_start'])

        script = script.replace("##VARS_INSERTED_HERE##",data)

      #script_path=os.path.join(tile_output_path , 'tile_{0}'.format(settings['tile']))

      try:
         os.mkdir(tile_output_path)
      except:
         pass

      f = open(script_path,"w")
      f.write(script)
      f.close()


      task_command = [
      str( app.config['BLENDER_PATH_LINUX'] ),
      '--background',
      str( file_path ),
      '--render-output',
      str(tile_output_path),
      '--python',
      str(script_path),
      '--frame-start' ,
      str(settings['frame_start']),
      '--frame-end',
      str(settings['frame_end']),
      '--render-format',
      str(settings['format']),
      '--render-anim',
      '--enable-autoexec'
      ]

      return task_command