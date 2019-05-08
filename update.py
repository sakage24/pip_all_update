#! /usr/bin/python3.7
from subprocess import run
from subprocess import CompletedProcess


class Module(object):
    @staticmethod
    def __get_list(pip_version: str = 'pip',
                   encoding: str = 'utf-8',
                   require_sudo: bool = False) -> list:
        """
            アップデートが必要なファイルリストを取得して、ファイル名だけをlistにして返す。
        """
        if require_sudo:
            check_command: str = f'sudo -H {pip_version} list --outdated'
        else:
            check_command: str = f'{pip_version} list --outdated'

        response: CompletedProcess = run(
            check_command.split(),
            check=True,
            capture_output=True,
        )

        result: list = response.stdout.decode(encoding).split()

        if result:
            # テーブルヘッダ、ボーダーなどの不要な部分とバージョン部分をカットして返却している
            return result[8::4]
        else:
            raise UpdateNotFoundError

    def write_list(self,
                   file_path: str = './requirements.txt',
                   pip_version: str = 'pip',
                   encoding: str = 'utf-8',
                   require_sudo: bool = False) -> bool:
        """
            __get_list関数の実行結果をテキストファイルとして書き出す
        """
        try:
            lists: list = self.__get_list(
                pip_version=pip_version,
                encoding=encoding,
                require_sudo=require_sudo,
            )
        except UpdateNotFoundError:
            return False
        else:
            with open(file_path, mode='wt', encoding=encoding) as f:
                for i in lists:
                    f.write(i + '\n')
            return True

    def update(self,
               pip_version: str = 'pip',
               encoding: str = 'utf-8',
               require_sudo: bool = False) -> None:
        """
            アップデートが必要なモジュールを調べて、
            必要なモジュールに対してのみアップデートコマンドを繰り返し実行する
        """
        try:
            lists: list = self.__get_list(
                pip_version=pip_version,
                encoding=encoding,
                require_sudo=require_sudo,
            )
        except UpdateNotFoundError as e:
            print(e)
        else:
            if require_sudo:
                update_command: str = f'sudo -H {pip_version} install -U'
            else:
                update_command: str = f'{pip_version} install -U'

            for i in lists:
                command: list = f"{update_command} {i}".split()
                response: CompletedProcess = run(
                    command,
                    check=True,
                    capture_output=True,
                )
                result: str = response.stdout.decode(encoding)
                print(result)


class UpdateNotFoundError(BaseException):
    def __str__(self):
        return 'アップデートが必要なpythonモジュールはありませんでした。'


if __name__ == '__main__':
    module = Module()
    versions: str = 'pip3.7'
    charset: str = 'utf-8'
    require_sudo: bool = True

    try:
        module.update(pip_version=versions,
                      encoding=charset,
                      require_sudo=require_sudo)
    except KeyboardInterrupt:
        print('ユーザによって処理が中断されました...')
    finally:
        print('全ての処理が完了しました...')
