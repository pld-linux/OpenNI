#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	java		# Java wrappers
%bcond_without	mono		# Mono/.NET wrappers
%bcond_with	sse2		# use SSE2 instructions
%bcond_with	sse3		# use SSE3 instructions
%bcond_with	ssse3		# use SSE3 and SSSE3 instructions

%if %{with ssse}
%define	with_sse3	1
%endif
Summary:	OpenNI framework for Natural Interaction devices
Summary(pl.UTF-8):	Szkielet OpenNI do urządzeń służących interakcji z naturą
Name:		OpenNI
Version:	1.5.7.10
Release:	1
License:	Apache v2.0
Group:		Libraries
Source0:	https://github.com/OpenNI/OpenNI/tarball/Stable-%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	5c6072e875a72180a696ee60460ba347
Patch0:		%{name}-system-libs.patch
Patch1:		%{name}-nosse.patch
URL:		http://openni.org/
BuildRequires:	OpenGL-devel
# for examples
BuildRequires:	OpenGL-glut-devel >= 3
%{?with_apidocs:BuildRequires:	doxygen}
%{?with_apidocs:BuildRequires:	graphviz}
%{?with_java:BuildRequires:	jdk >= 1.6.0}
BuildRequires:	libjpeg-devel
BuildRequires:	libstdc++-devel >= 6:4.0
BuildRequires:	libusb-devel >= 1.0.8
%{?with_mono:BuildRequires:	mono-csharp}
BuildRequires:	python >= 1:2.6
BuildRequires:	rpmbuild(macros) >= 1.566
BuildRequires:	sed >= 4.0
# NOTE: other platforms need adding a dozen of defines in Include/Linux-*/*.h
ExclusiveArch:	%{ix86} %{x8664} arm
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%ifarch %{ix86}
%define		openni_platform	x86
%endif
%ifarch %{x8664}
%define		openni_platform	x64
%endif
%ifarch arm
%define		openni_platform	Arm
%endif

%description
OpenNI framework provides an application programming interface (API)
for writing applications utilizing natural interaction. This API
covers communication with both low level devices (e.g. vision and
audio sensors), as well as high-level middleware solutions (e.g. for
visual tracking using computer vision).

The OpenNI Framework provides the interface for physical devices and
for middleware components. The API enables modules to be registered in
the OpenNI framework and used to produce sensory data. Selecting the
hardware or middleware module is easy and flexible.

%description -l pl.UTF-8
Szkielet OpenNI zapewnia interfejs programistyczny (API) dla aplikacji
wykorzystujących interakcję z naturą. API to pokrywa komunikację
zarówno z urządzeniami niskiego poziomu (takimi jak czujniki obrazu i
dźwięku), jak i rozwiązaniami wysokiego poziomu warstwy pośredniej
(np. do wizualnego śledzenia przy użyciu obrazu komputerowego).

Szkielet OpenNI zapewnia interfejs dla fizycznych urządzeń oraz
komponentów warstwy pośredniej. API pozwala na rejestrowanie modułów w
szkielecie OpenNI i wykorzystywanie do tworzenia danych sensorycznych.
Wybór sprzętu i modułu pośredniego jest prosty i elastyczny.

%package devel
Summary:	Header files for OpenNI library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki OpenNI
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for OpenNI library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki OpenNI.

%package doc
Summary:	OpenNI user guide
Summary(pl.UTF-8):	Podręcznik użytkownika OpenNI
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc
OpenNI user guide in PDF format.

%description doc -l pl.UTF-8
Podręcznik użytkownika OpenNI w formacie PDF.

%package apidocs
Summary:	OpenNI API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki OpenNI
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API and internal documentation for OpenNI library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki OpenNI.

%package -n java-OpenNI
Summary:	Java wrapper for OpenNI
Summary(pl.UTF-8):	Interfejs Javy do OpenNI
Group:		Libraries/Java
Requires:	%{name} = %{version}-%{release}
Requires:	jpackage-utils
Requires:	jre >= 1.6.0

%description -n java-OpenNI
Java wrapper for OpenNI.

%description -n java-OpenNI -l pl.UTF-8
Interfejs Javy do OpenNI.

%package -n dotnet-OpenNI
Summary:	.NET wrapper for OpenNI
Summary(pl.UTF-8):	Interfejs .NET do OpenNI
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	mono

%description -n dotnet-OpenNI
.NET wrapper for OpenNI.

%description -n dotnet-OpenNI -l pl.UTF-8
Interfejs .NET do OpenNI.

%prep
%setup -q -n %{name}-OpenNI-1e9524f
%undos Platform/Linux/Build/Samples/NiUserTracker/Makefile
%patch0 -p1
%patch1 -p1

%build
%{__make} -C Platform/Linux/Build clean
export CFLAGS="%{rpmcflags}"
%{__make} -C Platform/Linux/Build \
	CFG=PLD \
	CXX="%{__cxx}" \
	HOSTPLATFORM=%{openni_platform} \
	SSE_GENERATION=%{?with_sse3:3}%{!?with_sse3:%{?with_sse2:2}} \
	%{?with_ssse3:SSSE3_ENABLED=1} \
	%{!?with_mono:MONO_INSTALLED=0} \
	%{!?with_java:ALL_JAVA_PROJS= JAVA_SAMPLES=}

%if %{with apidocs}
cd Source/DoxyGen
doxygen Doxyfile
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_includedir}/ni,/var/lib/ni}

BDIR=Platform/Linux/Bin/%{openni_platform}-PLD
install -p ${BDIR}/ni{Reg,License} $RPM_BUILD_ROOT%{_bindir}
install -p ${BDIR}/libOpenNI.so $RPM_BUILD_ROOT%{_libdir}
install -p ${BDIR}/libnim{Codecs,MockNodes,Recorder}.so $RPM_BUILD_ROOT%{_libdir}
cp -p Include/*.h $RPM_BUILD_ROOT%{_includedir}/ni
%ifarch %{ix86} %{x8664}
cp -pr Include/Linux-x86 $RPM_BUILD_ROOT%{_includedir}/ni
%endif
%ifarch arm
cp -pr Include/Linux-Arm $RPM_BUILD_ROOT%{_includedir}/ni
%endif

%if %{with java}
install -d $RPM_BUILD_ROOT%{_javadir}
install -p ${BDIR}/libOpenNI.jni.so $RPM_BUILD_ROOT%{_libdir}
cp -p ${BDIR}/org.openni.jar $RPM_BUILD_ROOT%{_javadir}
%endif

%if %{with mono}
gacutil -i ${BDIR}/OpenNI.net.dll -package 2.0 -root $RPM_BUILD_ROOT%{_prefix}/lib
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
for mod in libnimMockNodes.so libnimCodecs.so libnimRecorder.so; do
	%{_bindir}/niReg -r %{_libdir}/$mod
done

%preun
if [ "$1" = "0" ]; then
	for mod in libnimMockNodes.so libnimCodecs.so libnimRecorder.so; do
		%{_bindir}/niReg -u %{_libdir}/$mod
	done
fi

%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES NOTICE README
%attr(755,root,root) %{_bindir}/niLicense
%attr(755,root,root) %{_bindir}/niReg
%attr(755,root,root) %{_libdir}/libOpenNI.so
%attr(755,root,root) %{_libdir}/libnimCodecs.so
%attr(755,root,root) %{_libdir}/libnimMockNodes.so
%attr(755,root,root) %{_libdir}/libnimRecorder.so
%dir /var/lib/ni

%files devel
%defattr(644,root,root,755)
%{_includedir}/ni

%files doc
%defattr(644,root,root,755)
%doc Documentation/OpenNI_UserGuide.pdf

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc Source/DoxyGen/html/*.{bmp,css,html,js,png}
%endif

%if %{with java}
%files -n java-OpenNI
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libOpenNI.jni.so
%{_javadir}/org.openni.jar
%endif

%if %{with mono}
%files -n dotnet-OpenNI
%defattr(644,root,root,755)
%{_prefix}/lib/mono/2.0/OpenNI.net.dll
%{_prefix}/lib/mono/gac/OpenNI.net
%endif
