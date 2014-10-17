%define rname	OpenIPMI
%define major	0
%define maj1	1
%define	libposix	%mklibname %{rname}posix %{major}
%define	libglib		%mklibname %{rname}glib %{major}
%define	libcmdlang	%mklibname %{rname}cmdlang %{major}
%define	libpthread	%mklibname %{rname}pthread %{major}
%define	libname		%mklibname %{rname} %{major}
%define	libutils	%mklibname %{rname}utils %{major}
%define	libui		%mklibname %{rname}ui %{maj1}
%define	liblanserv	%mklibname %{rname}lanserv %{major}
%define	libtcl		%mklibname %{rname}tcl %{major}
%define	devname		%mklibname %{rname} -d

%bcond_with	tcl
%bcond_with	tk

Summary: 	Library interface to IPMI
Name: 		openipmi
Version:	2.0.21
Release:	1
License: 	LGPLv2+
Group: 		System/Kernel and hardware
Url: 		http://openipmi.sourceforge.net
Source0: 	http://downloads.sourceforge.net/openipmi/%{rname}-%{version}.tar.gz
Source1:	openipmi.sysconf
Source2:	openipmi-helper
Source3:	ipmi.service
Source4:	openipmi.modalias

Patch3:		OpenIPMI-2.0.16-python26.patch
Patch4:		openipmi-2.0.16-pthreads.patch

BuildRequires:	swig >= 1.3
%if %{with tcl}
BuildRequires:	tcl
BuildRequires:	pkgconfig(tcl)
%endif
%if %{with tk}
BuildRequires:	tk
BuildRequires:	tkinter
BuildRequires:	pkgconfig(tk)
%endif
BuildRequires:	gdbm-devel
BuildRequires:	net-snmp-devel
BuildRequires:	perl-devel
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(popt)
BuildRequires:	pkgconfig(python2)
Requires(pre,post):	rpm-helper

%description 
This package contains a shared library implementation of IPMI and the
basic tools used with OpenIPMI.

%package -n perl-%{name}
Summary:	Perl interface for OpenIPMI
Group:		Development/Perl
Requires:	%{name} = %{version}-%{release}

%description -n perl-%{name}
A Perl interface for OpenIPMI.

%package -n python-%{name}
Summary:	Python interface for OpenIPMI
Group:		Development/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-%{name}
A Python interface for OpenIPMI.

%package gui
Summary:	GUI (in python) for OpenIPMI
Group:		System/Kernel and hardware
Requires:	python-%{name} = %{version}-%{release}
Requires:	wxPython >= 2.4.2
Requires:	wxPythonGTK

%description gui
A GUI interface for OpenIPMI.  Written in python an requiring wxWidgets.

%package ui
Summary:	User Interface (ui)
Group:		System/Kernel and hardware
Requires:	%{name} = %{version}-%{release}

%description ui
This package contains a user interface

%package lanserv
Summary:	Emulates an IPMI network listener
Group:		System/Kernel and hardware
Requires:	%{name} = %{version}-%{release}

%description lanserv
This package contains a network IPMI listener.

%package -n %{libcmdlang}
Summary:	A library for %{name}
Group:		System/Libraries

%description -n %{libcmdlang}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n %{libglib}
Summary:	A library for %{name}
Group:		System/Libraries

%description -n %{libglib}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n %{libposix}
Summary:	A library for %{name}
Group:		System/Libraries

%description -n %{libposix}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n %{libpthread}
Summary:	A library for %{name}
Group:		System/Libraries

%description -n %{libpthread}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n %{libname}
Summary:	A library for %{name}
Group:		System/Libraries

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n %{libutils}
Summary:	A library for %{name}
Group:		System/Libraries

%description -n %{libutils}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n %{libui}
Summary:	A library for %{name}
Group:		System/Libraries

%description -n %{libui}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n %{liblanserv}
Summary:	A library for %{name}
Group:		System/Libraries
Conflicts:	%{name}-lanserv < 2.0.18-5

%description -n %{liblanserv}
This package contains the library needed to run programs dynamically
linked with %{name}.

%if %{with tcl}
%package -n %{libtcl}
Summary:	A library for %{name}
Group:		System/Libraries
Obsoletes:	tcl-%{name} < 2.0.18-5

%description -n %{libtcl}
This package contains the library needed to run programs dynamically
linked with %{name}.
%endif

%package -n %{devname}
Summary:	Development files for OpenIPMI
Group:		Development/C
Requires:	%{libposix} = %{version}-%{release}
Requires:	%{libglib} = %{version}-%{release}
Requires:	%{libcmdlang} = %{version}-%{release}
Requires:	%{libpthread} = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libutils} = %{version}-%{release}
Requires:	%{libui} = %{version}-%{release}
Requires:	%{liblanserv} = %{version}-%{release}
%if %{with tcl}
Requires:	%{libtcl} = %{version}-%{release}
%endif
%rename		%{name}-devel < 2.0.18-5

%description -n %{devname}
Contains additional files need for a developer to create applications
and/or middleware that depends on libOpenIPMI

%prep
%setup -qn %{rname}-%{version}
%apply_patches

%build
export CFLAGS="`echo %{optflags} | sed 's/-Wp,-D_FORTIFY_SOURCE=2//'`"
export PYTHONDONTWRITEBYTECODE=
export PYTHON=%{python2}

%define _disable_ld_no_undefined 1
%configure	\
	--with-perlinstall=%{perl_vendorarch} \
	--with-pythoninstall=%{python2_sitearch} \
	--with-glib12=no \
%if !%{with tcl}
	--with-tcl=no \
%endif
%if !%{with tk}
	--with-tkinter=no \
%endif
	--with-pythonusepthreads=yes \
	--with-perlusepthreads=yes \
	--disable-static

%make

%install
%makeinstall_std PYTHON_GUI_DIR=openipmigui

find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'

install -d %{buildroot}%{_sysconfdir}/sysconfig
install -m 644 %SOURCE1 %{buildroot}%{_sysconfdir}/sysconfig/ipmi
install -d %{buildroot}%{_libexecdir}
install -m 755 %SOURCE2 %{buildroot}%{_libexecdir}/openipmi-helper
install -d %{buildroot}%{_unitdir}
install -m 644 %SOURCE3 %{buildroot}%{_unitdir}/ipmi.service
install -d %{buildroot}%{_sysconfdir}/modprobe.d
install -m 644 %SOURCE4 %{buildroot}%{_sysconfdir}/modprobe.d/OpenIPMI.conf
install -d %{buildroot}%{_localstatedir}/run/%{name}


%preun
%_preun_service ipmi

%postun
%_post_service ipmi

%files
%doc FAQ README README.Force
%doc README.MotorolaMXP
%{_sysconfdir}/init.d/ipmi
%config(noreplace) %{_sysconfdir}/sysconfig/ipmi

%files ui
%{_bindir}/ipmi_ui
%{_bindir}/ipmicmd
%{_bindir}/openipmicmd
%{_bindir}/ipmish
%{_bindir}/openipmish
%{_bindir}/solterm
%{_bindir}/rmcp_ping
%doc %{_mandir}/man1/ipmi_ui.1*
%doc %{_mandir}/man1/openipmicmd.1*
%doc %{_mandir}/man1/openipmish.1*
%doc %{_mandir}/man1/openipmigui.1*
%doc %{_mandir}/man1/solterm.1*
%doc %{_mandir}/man1/rmcp_ping.1*
%doc %{_mandir}/man7/ipmi_cmdlang.7*
%doc %{_mandir}/man7/openipmi_conparms.7*

%files lanserv
%{_bindir}/ipmilan
%doc %{_mandir}/man8/ipmilan.8*
%files -n %{libcmdlang}
%{_libdir}/libOpenIPMIcmdlang.so.%{major}*

%files -n perl-%{name}
%{perl_vendorarch}/OpenIPMI.pm
%{perl_vendorarch}/auto/OpenIPMI
%doc swig/OpenIPMI.i swig/perl/sample swig/perl/ipmi_powerctl

%files -n python-%{name}
%{python_sitearch}/*OpenIPMI.*
%doc swig/OpenIPMI.i

%files gui
%{python2_sitearch}/openipmigui/*
%{_bindir}/openipmigui

%files -n %{libglib}
%{_libdir}/libOpenIPMIglib.so.%{major}*

%files -n %{libposix}
%{_libdir}/libOpenIPMIposix.so.%{major}*

%files -n %{libpthread}
%{_libdir}/libOpenIPMIpthread.so.%{major}*

%files -n %{libname}
%{_libdir}/libOpenIPMI.so.%{major}*

%files -n %{libutils}
%{_libdir}/libOpenIPMIutils.so.%{major}*

%files -n %{libui}
%{_libdir}/libOpenIPMIui.so.%{maj1}*

%files -n %{liblanserv}
%{_libdir}/libIPMIlanserv.so.%{major}*

%if %{with tcl}
%files -n %{libtcl}
%{_libdir}/libOpenIPMItcl.so.%{major}*
%endif

%files -n %{devname}
%{_includedir}/OpenIPMI
%{_libdir}/*.so
%{_libdir}/pkgconfig
%doc doc/IPMI.pdf

