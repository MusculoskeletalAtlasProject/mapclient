import os
import subprocess
import tempfile

from mapclient.settings import version as app_version


class ReplaceOnlyDict(dict):

    def __missing__(self, key):
        return '{' + key + '}'


def run_build(pyi_config, spec_file, **kwargs):
    import PyInstaller.building.build_main
    PyInstaller.building.build_main.main(pyi_config, spec_file, **kwargs)


def run_command(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(p.stdout.readline, ''):
        yield stdout_line

    return_code = p.wait()
    yield 'command returned with value: %s' % return_code


def run_makensis(repo_root_dir):
    if not os.path.exists(os.path.join(repo_root_dir, 'package')):
        os.mkdir(os.path.join(repo_root_dir, 'package'))

    nsis_exe = os.path.join(os.environ['PROGRAMFILES(X86)'], 'NSIS', 'BIN', 'makensis.exe')
    if os.path.exists(nsis_exe):
        # Create NSIS script from template
        with tempfile.NamedTemporaryFile(delete=False) as outputfile:
            with open(os.path.join(repo_root_dir, 'res', 'win', 'nsis.nsi.template')) as f:
                contents = f.read()

            match_keys = ReplaceOnlyDict(map_client_version=app_version.__version__,
                                         dist_dir=os.path.join(repo_root_dir, 'dist'),
                                         win_res_dir=os.path.join(repo_root_dir, 'res', 'win'),
                                         package_dir=os.path.join(repo_root_dir, 'package'))
            formatted_contents = contents.format_map(match_keys)
            outputfile.write(formatted_contents.encode())
            outputfile.flush()
            # os.chdir(os.path.join(repo_root_dir, 'res', 'win'))
            for line in run_command([nsis_exe, outputfile.name]):
                print(line.strip())

        if os.path.isfile(outputfile.name):
            os.remove(outputfile.name)


if __name__ == '__main__':
    '''
    Create a Windows application installer with NSIS and pyinsatller.
    '''
    abs_script_directory = os.path.realpath(os.path.dirname(__file__))

    src_root_dir = os.path.realpath(os.path.join(abs_script_directory, '..'))
    repo_root_dir = os.path.realpath(os.path.join(src_root_dir, '..'))

    os.environ['MAPCLIENT_REPOROOT'] = repo_root_dir
    options = {
        'noconfirm': True,
        'distpath': repo_root_dir,
        'workpath': repo_root_dir,
        'clean_build': True,
    }

    run_build(None, os.path.join(repo_root_dir, 'res', 'win', 'mapclient_pyinstaller.spec'), noconfirm=options['noconfirm'],
              distpath=options['distpath'], workpath=options['workpath'], clean_build=options['clean_build'])

    run_makensis(repo_root_dir)
