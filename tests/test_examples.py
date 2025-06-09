

def test_example_1():
    from runtime.application import (
        single_instance, is_interactive, get_main_package,
        hook_terminate, TerminateException
    )
    from runtime.user import get_username, is_elevated

    hook_terminate()
    username = get_username()
    pkg = get_main_package()
    interactive = is_interactive()

    def output(line: str):
        if interactive:
            print(line)


    with single_instance():
        try:
            output(f"Hello {'admin ' if is_elevated() else ''}{username}, this is {pkg.name} ver. {pkg.version}")
        except TerminateException:
            output(f"Bye {username}")
        except:
            output("An unexpected error ocurred")