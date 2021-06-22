from mdl.downloader import MangaDownloader
from mdl.fileio import FileIo

print('\n'
      '1) Enter a URL\n'
      '2) Create Library\n'
      '3) Check in library\n'
      '4) Update Library\n'
      '5) Select from library\n'
      '6) Clear(Delete) Library\n')

try:
    choice = int(input('What do you want to do: '))
except ValueError:
    choice = 0
except KeyboardInterrupt:
    choice = 0

downloader = MangaDownloader()
file = FileIo()

if choice == 1:

    _manga = downloader.manga

    urls = _manga['urls']
    filenames = _manga['filenames']

    try:
        for count in range(int(input('How many chapters?: '))):
            link = input(f'{count + 1}) URL: ')
            if not link == '':
                downloader.source = link.split('.')[1]
                fname = downloader.get_filename(link)
                urls.append(link.strip())
                filenames.append(fname.strip())

    except KeyboardInterrupt:
        print('\nInput aborted. downloading given URLs instead...')

    except ValueError:
        print('please enter a number')
        exit()

    downloader.download_manga()

elif choice == 2:
    file.create()
    i = 1

    try:
        while True:
            url = input(f'{i}) ')
            if url != '':
                file.dump(url)
            else:
                break
            i += 1
    except KeyboardInterrupt:
        exit()

    except ValueError:
        print('Invalid Characters?')
        exit()

elif choice == 3:
    entries = file.read()
    if entries != '':
        print('\n' + file.read())

elif choice == 4:
    i = 1

    while True:
        url = input(f'{i}) ')
        if url != '':
            file.dump(url)
        else:
            break
        i += 1

elif choice == 5:

    entries = file.read()

    if entries != '':
        print(f'\n{entries}')
        entries = entries.splitlines()

        try:
            entryno = int(input('Select Entry: ')) - 1
            chapter = int(input('Enter chapter: '))
            url = entries[entryno].split('>')[-1].strip()
            optional_string = (''.join(entries[entryno].split('>')[:-1])).strip().lower().replace(' ', '-')

            if url.split('.')[1] == 'readm':
                url += f'/{chapter}' + '/all-pages'
            elif url.split('.')[1] == 'manganelo':
                url += f'/chapter-{chapter}'
            else:
                print('\nNOPE\n')
                exit()

            downloader.manga['urls'].append(url)
            downloader.manga['filenames'].append(downloader.get_filename(url=url, optional_string=optional_string))

            downloader.download_manga()

        except ValueError:
            print('no entry selected. quiting')
            exit()

elif choice == 6:
    try:
        file.delete()
    except FileNotFoundError:
        print('Can\'t delete a non-existent file.')

else:
    if choice == 0:
        print('Invalid choice')
        exit()
