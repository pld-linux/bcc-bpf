#
# Conditional build:
%bcond_without	lua		# build without tests

# luajit is not available for some architectures
%ifnarch %{ix86} %{x8664} %{arm} mips ppc
%undefine	with_lua
%endif

Summary:	Tools for BPF-based Linux IO analysis, networking, monitoring, and more
Name:		bcc-bpf
Version:	0.7.0
Release:	0.1
License:	Apache v2.0
Group:		Applications
Source0:	https://github.com/iovisor/bcc/archive/v%{version}/bcc-%{version}.tar.gz
# Source0-md5:	79a445aa6542bcc260fd38af3402a77d
URL:		https://iovisor.github.io/bcc/
BuildRequires:	bison
BuildRequires:	cmake >= 2.8.7
BuildRequires:	elfutils-libelf-devel-static
BuildRequires:	flex
BuildRequires:	gcc
BuildRequires:	libstdc++-devel
%{?with_lua:BuildRequires: pkgconfig(luajit)}
BuildRequires:	python-devel
ExclusiveArch:	%{ix86} %{x8664} power64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
BCC is a toolkit for creating efficient kernel tracing and
manipulation programs, and includes several useful tools and examples.
It makes use of extended BPF (Berkeley Packet Filters), formally known
as eBPF, a new feature that was first added to Linux 3.15. BCC makes
BPF programs easier to write, with kernel instrumentation in C (and
includes a C wrapper around LLVM), and front-ends in Python and LUA.

It is suited for many tasks, including performance analysis and
network traffic control.

%package libs
Summary:	Shared Library for BPF Compiler Collection (BCC)
Group:		Libraries

%description libs
Shared Library for BPF Compiler Collection (BCC)

%package -n python-%{name}
Summary:	Python bindings to %{name}
Group:		Libraries/Python

%description -n python-%{name}
Python bindings for BPF Compiler Collection (BCC)

%package tools
Summary:	Tools for BPF Compiler Collection (BCC)
Group:		Applications

%description tools
Command line tools for BPF Compiler Collection (BCC)

%package -n lua-%{name}
Summary:	LUA bindings to %{name}
Group:		Applications

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
