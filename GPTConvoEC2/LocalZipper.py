import os
import zipfile
import shutil
from datetime import datetime
from collections import defaultdict

class LocalFileZipper:
    def __init__(self):
        pass


    def _local_walk(self, localpath):
        for dirpath, dirnames, filenames in os.walk(localpath):
            yield dirpath, dirnames, filenames


    def zipFiles(self, localDir, unityScript, character_order, downloads_dir="/home/ubuntu/gptconvo/ScriptsDropoff/"):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        zip_file_name = 'script_' + timestamp + '.zip'
        zip_file_path = os.path.join(downloads_dir, zip_file_name)

        character_files = defaultdict(list)

        for dirpath, dirnames, filenames in self._local_walk(localDir):
            for filename in filenames:
                if filename != '.gitkeep':
                    file_path = os.path.join(dirpath, filename)
                    character = os.path.basename(dirpath)
                    character_files[character].append(file_path)

        for character in character_files:
            character_files[character].sort()

        with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            with open('script.txt', 'w') as temp_file:
                temp_file.write(unityScript)

            zf.write('script.txt')

            for i, character in enumerate(character_order):
                if character_files[character]:
                    file_path = character_files[character].pop(0)
                    new_filename = f"{character}_{str(i).zfill(5)}.wav"
                    zf.write(file_path, new_filename)

            os.remove('script.txt')

        print(f'Files from {localDir} and script.txt have been zipped and saved to {zip_file_path}')

        self.deleteResults()


    def deleteResults(self, localDir='/home/ubuntu/gptconvo/ai-voice-cloning/results/'):
        try:
            # delete all files and directories except for .gitkeep
            for dirpath, dirnames, filenames in self._local_walk(localDir):
                for filename in filenames:
                    if filename != ".gitkeep":
                        os.remove(os.path.join(dirpath, filename))
                for dirname in dirnames:
                    shutil.rmtree(os.path.join(dirpath, dirname))

                print(f'Files and directories in {localDir}, except for .gitkeep, have been deleted.')
        except Exception as e:
            print(f"Error deleting files or directories: {e}")

