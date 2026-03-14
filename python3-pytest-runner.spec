#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests (require network)

Summary:	Invoke py.test as distutils command with dependency resolution
Summary(pl.UTF-8):	Wywoływanie py.test jako polecenia distutils z rozwiązywaniem zależności
Name:		python3-pytest-runner
Version:	6.0.1
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pytest-runner/
Source0:	https://files.pythonhosted.org/packages/source/p/pytest-runner/pytest-runner-%{version}.tar.gz
# Source0-md5:	bd11f67561d7c4db8cf7e96b13ab469f
URL:		https://github.com/pytest-dev/pytest-runner
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.7
BuildRequires:	python3-setuptools >= 1:56
BuildRequires:	python3-setuptools_scm >= 3.4.1
%if %{with tests}
BuildRequires:	python3-pytest >= 6
# optional/lint only
#BuildRequires:	python3-pytest-checkdocs >= 2.4
#BuildRequires:	python3-pytest-black >= 0.3.7
#BuildRequires:	python3-pytest-cov
#BuildRequires:	python3-pytest-enabler >= 1.0.1
#BuildRequires:	python3-pytest-flake8
#BuildRequires:	python3-pytest-mypy >= 0.9.1
BuildRequires:	python3-pytest-virtualenv
%endif
%if %{with doc}
BuildRequires:	python3-jaraco.packaging >= 9
BuildRequires:	python3-jaraco.tidelift >= 1.4
BuildRequires:	python3-rst.linker >= 1.9
BuildRequires:	sphinx-pdg-3
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
Requires:	python3-modules >= 1:3.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Setup scripts can use pytest-runner to add setup.py test support for
pytest runner.

%description -l pl.UTF-8
Skrypty setup mogą wykorzystywać moduł pytest-runner do dodawania
obsługi testów pytest runnera w setup.py.

%package apidocs
Summary:	pytest-runner module documentation
Summary(pl.UTF-8):	Dokumentacja modułu pytest-runner
Group:		Documentation

%description apidocs
Documentation for pytest-runner module.

%description apidocs -l pl.UTF-8
Dokumentacja modułu pytest-runner.

%prep
%setup -q -n pytest-runner-%{version}

%build
%py3_build_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_virtualenv \
%{__python3} -m pytest ptr tests
%endif

%if %{with doc}
sphinx-build-3 -b html docs docs/build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE README.rst
%{py3_sitescriptdir}/ptr
%{py3_sitescriptdir}/pytest_runner-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_static,*.html,*.js}
%endif
