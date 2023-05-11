def get_packages(language='python'):
    """ populate available packages from the pip registry """
    app = get_application()
    if language == 'r':
        registry = "https://cran.r-project.org/web/packages/available_packages_by_name.html#available-packages-Z"
    elif language == 'conda':
        registry = app.config["CONDA_PYTHON_URL_ES"]
    elif language == "conda-r":
        registry = app.config["CONDA_R_URL_ES"]
    else:
        registry = app.config["PYPI_URL"]
    response = requests.get(registry) 
    response.raise_for_status()
    html_tree = html.fromstring(response.content)
    # pylint: disable=unnecessary-comprehension
    packages = [generate_packages(package, app.config['ARTIFACTORY'], language)
                for package in html_tree.xpath('//a/text()')
                if generate_packages(package, app.config['ARTIFACTORY'], language) is not None]

    # Remove redundant packages & versions pair
    if language == 'conda':
        packages = [i for n, i in enumerate(packages) if i not in packages[n + 1:]]
    return packages


# pylint: disable=inconsistent-return-statements
def generate_packages(package, artifactory, language):
    """ generate dict object for all the packages """
    if artifactory and language == 'r':
        if package.endswith('.tar.gz'):
            package_name = package.split("_")[0]
            package_version = re.search('_(.*).tar', package).group(1)
            return {"name": package_name, "version": package_version}
    elif language in ["conda", "conda-r"]:
        if package.endswith('tar.bz2'):
            package_name_list = package.split("-")
            build_name = package_name_list[-1]
            package_version = package_name_list[-2]
            package_name = "-".join(package_name_list[:-2])
            py_version = re.search("(py[0-9]{2})+", build_name)
            py_version = py_version.group() if py_version else "NA"
            if language == "conda":
                return {"name": package_name, "version": package_version, "python_version": py_version}
            return {"name": package_name}
    else:
        return {"name": package}
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