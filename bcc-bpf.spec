#
# Conditional build:
%bcond_without	lua		# lua
%bcond_without	python	# python

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
Patch0:		mandir.patch
URL:		https://iovisor.github.io/bcc/
BuildRequires:	bison
BuildRequires:	cmake >= 2.8.7
BuildRequires:	elfutils-libelf
BuildRequires:	elfutils-devel
BuildRequires:	flex
BuildRequires:	gcc
BuildRequires:	libstdc++-devel
BuildRequires:	llvm-devel
BuildRequires:	clang-devel
BuildRequires:	ncurses-devel
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

%package devel
Summary:	Shared library for BPF Compiler Collection (BCC)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing application that use BPF Compiler Collection (BCC).

%package -n python-%{name}
Summary:	Python bindings to %{name}
Group:		Libraries/Python
Requires:	%{name}-libs = %{version}-%{release}

%description -n python-%{name}
Python bindings for BPF Compiler Collection (BCC)

%package tools
Summary:	Tools for BPF Compiler Collection (BCC)
Group:		Applications
Requires:	%{name}-libs = %{version}-%{release}

%description tools
Command line tools for BPF Compiler Collection (BCC)

%package -n lua-%{name}
Summary:	LUA bindings to %{name}
Group:		Applications
Requires:	%{name}-libs = %{version}-%{release}

%description -n lua-%{name}
Standalone tool to run BCC tracers written in Lua

%prep
%setup -q -n bcc-%{version}
%patch -P0 -p1

%build
install -d build
cd build
%cmake \
	-DREVISION=%{version} \
	-DREVISION_LAST=%{version} \
	..
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/bcc/tools/old

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files libs
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/libbcc.so.*.*.*
%ghost %{_libdir}/libbcc.so.0
%attr(755,root,root) %{_libdir}/libbpf.so.*.*.*
%ghost %{_libdir}/libbpf.so.0

%files devel
%defattr(644,root,root,755)
%{_libdir}/libbpf.so
%{_libdir}/libbcc.so
%{_includedir}/bcc
%{_pkgconfigdir}/libbcc.pc

%files tools
%defattr(644,root,root,755)
%dir %{_datadir}/bcc
%{_datadir}/bcc/examples
%{_datadir}/bcc/introspection
%{_datadir}/bcc/tools
%{_mandir}/man8/argdist.8*
%{_mandir}/man8/bashreadline.8*
%{_mandir}/man8/biolatency.8*
%{_mandir}/man8/biosnoop.8*
%{_mandir}/man8/biotop.8*
%{_mandir}/man8/bitesize.8*
%{_mandir}/man8/bpflist.8*
%{_mandir}/man8/bps.8*
%{_mandir}/man8/btrfsdist.8*
%{_mandir}/man8/btrfsslower.8*
%{_mandir}/man8/cachestat.8*
%{_mandir}/man8/cachetop.8*
%{_mandir}/man8/capable.8*
%{_mandir}/man8/cobjnew.8*
%{_mandir}/man8/cpudist.8*
%{_mandir}/man8/cpuunclaimed.8*
%{_mandir}/man8/criticalstat.8*
%{_mandir}/man8/dbslower.8*
%{_mandir}/man8/dbstat.8*
%{_mandir}/man8/dcsnoop.8*
%{_mandir}/man8/dcstat.8*
%{_mandir}/man8/deadlock_detector.8*
%{_mandir}/man8/execsnoop.8*
%{_mandir}/man8/ext4dist.8*
%{_mandir}/man8/ext4slower.8*
%{_mandir}/man8/filelife.8*
%{_mandir}/man8/fileslower.8*
%{_mandir}/man8/filetop.8*
%{_mandir}/man8/funccount.8*
%{_mandir}/man8/funclatency.8*
%{_mandir}/man8/funcslower.8*
%{_mandir}/man8/gethostlatency.8*
%{_mandir}/man8/hardirqs.8*
%{_mandir}/man8/inject.8*
%{_mandir}/man8/javacalls.8*
%{_mandir}/man8/javaflow.8*
%{_mandir}/man8/javagc.8*
%{_mandir}/man8/javaobjnew.8*
%{_mandir}/man8/javastat.8*
%{_mandir}/man8/javathreads.8*
%{_mandir}/man8/killsnoop.8*
%{_mandir}/man8/llcstat.8*
%{_mandir}/man8/mdflush.8*
%{_mandir}/man8/memleak.8*
%{_mandir}/man8/mountsnoop.8*
%{_mandir}/man8/mysqld_qslower.8*
%{_mandir}/man8/nfsdist.8*
%{_mandir}/man8/nfsslower.8*
%{_mandir}/man8/nodegc.8*
%{_mandir}/man8/nodestat.8*
%{_mandir}/man8/offcputime.8*
%{_mandir}/man8/offwaketime.8*
%{_mandir}/man8/oomkill.8*
%{_mandir}/man8/opensnoop.8*
%{_mandir}/man8/phpcalls.8*
%{_mandir}/man8/phpflow.8*
%{_mandir}/man8/phpstat.8*
%{_mandir}/man8/pidpersec.8*
%{_mandir}/man8/profile.8*
%{_mandir}/man8/pythoncalls.8*
%{_mandir}/man8/pythonflow.8*
%{_mandir}/man8/pythongc.8*
%{_mandir}/man8/pythonstat.8*
%{_mandir}/man8/reset-trace.8*
%{_mandir}/man8/rubycalls.8*
%{_mandir}/man8/rubyflow.8*
%{_mandir}/man8/rubygc.8*
%{_mandir}/man8/rubyobjnew.8*
%{_mandir}/man8/rubystat.8*
%{_mandir}/man8/runqlat.8*
%{_mandir}/man8/runqlen.8*
%{_mandir}/man8/runqslower.8*
%{_mandir}/man8/slabratetop.8*
%{_mandir}/man8/softirqs.8*
%{_mandir}/man8/sslsniff.8*
%{_mandir}/man8/stackcount.8*
%{_mandir}/man8/statsnoop.8*
%{_mandir}/man8/syncsnoop.8*
%{_mandir}/man8/syscount.8*
%{_mandir}/man8/tcpaccept.8*
%{_mandir}/man8/tcpconnect.8*
%{_mandir}/man8/tcpconnlat.8*
%{_mandir}/man8/tcpdrop.8*
%{_mandir}/man8/tcplife.8*
%{_mandir}/man8/tcpretrans.8*
%{_mandir}/man8/tcpstates.8*
%{_mandir}/man8/tcpsubnet.8*
%{_mandir}/man8/tcptop.8*
%{_mandir}/man8/tcptracer.8*
%{_mandir}/man8/tplist.8*
%{_mandir}/man8/trace.8*
%{_mandir}/man8/ttysnoop.8*
%{_mandir}/man8/ucalls.8*
%{_mandir}/man8/uflow.8*
%{_mandir}/man8/ugc.8*
%{_mandir}/man8/uobjnew.8*
%{_mandir}/man8/ustat.8*
%{_mandir}/man8/uthreads.8*
%{_mandir}/man8/vfscount.8*
%{_mandir}/man8/vfsstat.8*
%{_mandir}/man8/wakeuptime.8*
%{_mandir}/man8/xfsdist.8*
%{_mandir}/man8/xfsslower.8*
%{_mandir}/man8/zfsdist.8*
%{_mandir}/man8/zfsslower.8*

%if %{with lua}
%files -n lua-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/bcc-lua
%endif

%if %{with python}
%files -n python-%{name}
%defattr(644,root,root,755)
%{py_sitedir}/bcc
%{py_sitedir}/bcc-*-py*.egg-info
%endif
