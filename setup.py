try:
    import subprocess
    import sys


    def install(package):
        subprocess.check_call([sys.executable, "-m", "pip", "install", package, '--upgrade'])


    print('Checking Modules..')

    modules = ['requests', 'bs4', 'pillow']

    for module in modules:
        try:
            __import__(module)
        except ModuleNotFoundError:
            install(module)

except ModuleNotFoundError:
    print('Something is wrong with your python installation.\nMake sure you have installed python properly')

except subprocess.CalledProcessError as err:
    print(f'{err}')
