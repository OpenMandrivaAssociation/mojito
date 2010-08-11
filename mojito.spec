%define major           0
%define libname         %mklibname %{name} %{major}
%define develname       %mklibname %{name} -d

%define client_major    1
%define client_name     %{name}-client
%define client_libname  %mklibname %{client_name} %{major}

Name: mojito
Summary: A social data aggregator library
Group: System/Libraries
Version: 0.26.1
License: LGPL 2.1
URL: http://www.moblin.org
Release: %mkrel 3
Source0: http://git.moblin.org/cgit.cgi/%{name}/snapshot/%{name}-%{version}.tar.gz
Patch0: mojito-0.26.1-facebook.patch
Patch1: mojito-0.21.2-persona.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires: glib2-devel
BuildRequires: libsoup-devel
BuildRequires: libGConf2-devel
BuildRequires: libdbus-glib-devel
BuildRequires: libgnome-keyring-devel
BuildRequires: intltool
BuildRequires: twitter-glib-devel
BuildRequires: librest-devel >= 0.3

%description
Social data aggregator for Moblin

%package -n %{libname}
Summary: Moblin's social data aggregator library
Group: System/Libraries
Requires: %{name} = %{version}-%{release}

%description -n %{libname}
Social data aggregator for Moblin

%package -n %{client_libname}
Summary: Moblin's social data aggregator client library
Group: System/Libraries
Requires: %{name} = %{version}-%{release}

%description -n %{client_libname}
Social data aggregator for Moblin

%package -n %{develname}
Summary: Mojito development environment
Group: System/Libraries
Requires: %{libname} = %{version}-%{release}
Requires: %{client_libname} = %{version}-%{release}
Provides: %{name}-devel

%description -n %{develname}
Header files and libraries for Mojito

%prep
%setup -q
%patch0 -p1 -b .facebook
%patch1 -p1 -b .persona
perl -pi -e 's,&& ./configure.*,,' ./autogen.sh

%build

#
# we need API keys for each service provided by moblin,
# the key used below for last.fm is actually upstream.
#

./autogen.sh
%configure2_5x	--prefix=/usr \
		--with-online=connman \
		--enable-myspace-key \
		--enable-flickr-key=1d92d04278e17e65aba27bcbca8995f4:9635a61d1c429528 \
		--enable-facebook-key=590293b6aeda63685cddadad022339b8:a2e9e0ec4b4215172c250d6fbdc64d55 \
		--enable-twitter-key=0YUkjT5HORHSuTs8oNcSzw:EWEqygCU1PavOrl6Cu0zUP4ajvSqeWSbqEAZx5WHis \
		--enable-lastfm-key
%make

%install
rm -rf %{buildroot}
%makeinstall_std
%find_lang %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING ChangeLog README NEWS TODO AUTHORS
%{_libdir}/mojito/services/*.so
%{_libdir}/mojito-core
%{_datadir}/dbus-1/services/mojito.service
%{_datadir}/mojito/services/*.keys
%{_datadir}/mojito/services/*.png

%files -n %{libname}
%defattr(-,root,root,-)
%{_libdir}/libmojito*.so.%{major}*

%files -n %{client_libname}
%defattr(-,root,root,-)
%{_libdir}/libmojito-client.so.%{client_major}*

%files -n %{develname}
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/mojito/services/*.la
%{_libdir}/mojito/services/*.a
%{_includedir}/mojito/*
%{_libdir}/pkgconfig/*.pc
