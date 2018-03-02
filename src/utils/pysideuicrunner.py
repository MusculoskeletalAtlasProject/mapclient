import sys

import os
from pysideuic import compileUi


if __name__ == '__main__':
    '''
    A '.ui' file is expected to be passed in as the first argument to this script.  The file should be described
    relative to the src directory of the repository.  The generated file will be output to a 'ui' directory at the same
    level as the input file and prefixed with 'ui_'.
    
    Script has been used with the following arguments:
     - mapclient/view/managers/options/qt/optionsdialog.ui
    '''
    if len(sys.argv) > 1:
        ui_file = sys.argv[1]
    else:
        print('Error: must supply filename through the command line.')
        sys.exit(-1)

    file_basename = os.path.basename(ui_file)
    file_root_name = os.path.splitext(file_basename)[0]
    abs_script_directory = os.path.realpath(os.path.dirname(__file__))

    src_root_dir = os.path.realpath(os.path.join(abs_script_directory, '..'))
    os.chdir(src_root_dir)
    abs_path_to_file = os.path.join(src_root_dir, ui_file)

    ui_file_directory = os.path.dirname(ui_file)
    ui_file_parent_directory = os.path.dirname(ui_file_directory)

    ui_file_output_directory = os.path.join(ui_file_parent_directory, 'ui')

    if not os.path.exists(os.path.join(src_root_dir, ui_file_output_directory)):
        print('Error: output directory "%s" does not exist.' % (os.path.join(src_root_dir, ui_file_output_directory)))
        sys.exit(-2)

    abs_path_to_ui_file = os.path.join(src_root_dir, ui_file_output_directory, 'ui_' + file_root_name + '.py')

    with open(ui_file, 'r') as f:
        with open(abs_path_to_ui_file, 'w') as g:
            print('Compiling ui file "%s" and saving in "%s".' % (abs_path_to_file, abs_path_to_ui_file))
            compileUi(f, g, from_imports=True)
