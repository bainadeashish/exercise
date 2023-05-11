def create_index(refresh=False, language='python'):
    """ Create ES index """
    if language == 'r':
        alias_name = 'cran
        packages = get_packages(language)

    package_list = []

    # pylint: disable=unexpected-keyword-arg
    for package in packages:
        if "href=" not in package:
            save_package_data(package, language)
            package_list.append(package['name'])

    if len(package_list) > 0:
        delete_missing_packages(package_list, language)