import Chan
import argparse


def main():
    parser = argparse.ArgumentParser(description='Lists or downloads Chan threads media links.')
    parser.add_argument('-list', metavar='Thread URL', type=str,
                        help='Lists all media links from the thread.')
    parser.add_argument('-download', metavar='Thread URL', type=str,
                        help='Downloads all media from the thread.')

    args = parser.parse_args()

    if args.list:
        chanDownloader = Chan.ChanDownloader(args.list)

        print(chanDownloader.urls)
    elif args.download:
        chanDownloader = Chan.ChanDownloader(args.download)

        chanDownloader.download()
    else:
        raise Exception('Something went wrong.')


if __name__ == '__main__':
    main()
