#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeframever	6.7
%define		qtver		5.15.2
%define		kfname		ktexteditor

Summary:	Full text editor component
Name:		kf6-%{kfname}
Version:	6.7.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	8f2cb0d135a01e221817d9ced984c325
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6DBus-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= %{qtver}
BuildRequires:	Qt6Network-devel >= %{qtver}
BuildRequires:	Qt6PrintSupport-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= %{qtver}
BuildRequires:	Qt6Widgets-devel >= %{qtver}
BuildRequires:	Qt6Xml-devel >= %{qtver}
BuildRequires:	cmake >= 3.16
BuildRequires:	gettext-devel
BuildRequires:	kf6-attica-devel >= %{version}
BuildRequires:	kf6-extra-cmake-modules >= %{version}
BuildRequires:	kf6-karchive-devel >= %{version}
BuildRequires:	kf6-kauth-devel >= %{version}
BuildRequires:	kf6-kbookmarks-devel >= %{version}
BuildRequires:	kf6-kcodecs-devel >= %{version}
BuildRequires:	kf6-kcompletion-devel >= %{version}
BuildRequires:	kf6-kconfig-devel >= %{version}
BuildRequires:	kf6-kconfigwidgets-devel >= %{version}
BuildRequires:	kf6-kcoreaddons-devel >= %{version}
BuildRequires:	kf6-kdbusaddons-devel >= %{version}
BuildRequires:	kf6-kglobalaccel-devel >= %{version}
BuildRequires:	kf6-kguiaddons-devel >= %{version}
BuildRequires:	kf6-ki18n-devel >= %{version}
BuildRequires:	kf6-kiconthemes-devel >= %{version}
BuildRequires:	kf6-kio-devel >= %{version}
BuildRequires:	kf6-kitemviews-devel >= %{version}
BuildRequires:	kf6-kjobwidgets-devel >= %{version}
BuildRequires:	kf6-knotifications-devel >= %{version}
BuildRequires:	kf6-kparts-devel >= %{version}
BuildRequires:	kf6-kservice-devel >= %{version}
BuildRequires:	kf6-ktextwidgets-devel >= %{version}
BuildRequires:	kf6-kwidgetsaddons-devel >= %{version}
BuildRequires:	kf6-kwindowsystem-devel >= %{version}
BuildRequires:	kf6-kxmlgui-devel >= %{version}
BuildRequires:	kf6-solid-devel >= %{version}
BuildRequires:	kf6-sonnet-devel >= %{version}
BuildRequires:	kf6-syntax-highlighting-devel >= %{version}
BuildRequires:	libgit2-devel
BuildRequires:	ninja
BuildRequires:	perl-base
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	kf6-dirs
#Obsoletes:	kf5-%{kfname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
KTextEditor provides a powerful text editor component that you can
embed in your application, either as a KPart or using the
KF6::TextEditor library (if you need more control).

The text editor component contains many useful features, from syntax
highlighting and automatic indentation to advanced scripting support,
making it suitable for everything from a simple embedded text-file
editor to an advanced IDE.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	kf6-kparts-devel >= %{kdeframever}
Requires:	kf6-syntax-highlighting-devel >= %{kdeframever}
#Obsoletes:	kf5-%{kfname}-devel < %{version}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

install -d $RPM_BUILD_ROOT%{_datadir}/katepart5/syntax

%find_lang %{kfname}6

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kfname}6.lang
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/ktexteditor-script-tester6
%ghost %{_libdir}/libKF6TextEditor.so.6
%attr(755,root,root) %{_libdir}/libKF6TextEditor.so.*.*
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/parts/katepart.so
%attr(755,root,root) %{_prefix}/libexec/kf6/kauth/kauth_ktexteditor_helper
%{_datadir}/dbus-1/system-services/org.kde.ktexteditor6.katetextbuffer.service
%{_datadir}/dbus-1/system.d/org.kde.ktexteditor6.katetextbuffer.conf
%{_datadir}/kdevappwizard/templates/ktexteditor6-plugin.tar.bz2
%{_datadir}/qlogging-categories6/ktexteditor.categories
%{_datadir}/qlogging-categories6/ktexteditor.renamecategories
%{_datadir}/polkit-1/actions/org.kde.ktexteditor6.katetextbuffer.policy

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF6/KTextEditor
%{_libdir}/cmake/KF6TextEditor
%{_libdir}/libKF6TextEditor.so
