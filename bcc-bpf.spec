Summary:	Tools for BPF-based Linux IO analysis, networking, monitoring, and more
Name:		bcc-bpf
Version:	0.2.0
Release:	0.1
License:	Apache v2.0
Group:		Development/Languages
URL:		https://github.com/iovisor/bcc
Source0:	https://github.com/iovisor/bcc/archive/v%{version}.tar.gz
# Source0-md5:	eed71341f397c72a50b45b376060b17d
BuildRequires:	bison
BuildRequires:	cmake >= 2.8.7
BuildRequires:	elfutils-libelf-devel-static
BuildRequires:	flex
BuildRequires:	gcc
BuildRequires:	libstdc++-devel
BuildRequires:	python-devel

%description
Python bindings for BPF Compiler Collection (BCC). Control a BPF
program from userspace.

%package libs
%description libs
Shared Library for BPF Compiler Collection (BCC)

%package -n python-%{name}
Summary:	Python bindings to %{name}
Summary:	libraries for %{name}

%description -n python-%{name}
Python bindings for BPF Compiler Collection (BCC)

%package tools
Summary:	Tools for BPF Compiler Collection (BCC)

%description tools
Command line tools for BPF Compiler Collection (BCC)

%package -n lua-%{name}
Summary:	LUA bindings to %{name}

%description -n lua-%{name}
Standalone tool to run BCC tracers written in Lua

%prep
%setup -q -n bcc-%{version}

%build
install -d build
cd build
%cmake ..
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files -n python-%{name}
%defattr(644,root,root,755)
%{py_sitescriptdir}/bcc*

%files libs
%defattr(644,root,root,755)
%{_libdir}/*
%{_includedir}/bcc/*

%files tools
%defattr(644,root,root,755)
%{_datadir}/bcc/tools/*
%{_datadir}/bcc/man/*

%files -n lua-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/bcc-lua
