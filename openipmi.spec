%define _disable_ld_no_undefined 1

%define realname OpenIPMI

#The lib naming in OpenIPMI 1.x
%define oldlibname %mklibname %realname 1

Name: 		openipmi
Summary: 	%{name} - Library interface to IPMI
Version:	2.0.14
Release:	%mkrel 5
License: 	LGPLv2+
Group: 		System/Kernel and hardware
URL: 		http://openipmi.sourceforge.net
Source: 	http://downloads.sourceforge.net/openipmi/%{realname}-%{version}.tar.bz2
BuildRequires:	swig >= 1.3
BuildRequires:	python-devel
BuildRequires:	popt-devel
BuildRequires:	ncurses-devel
BuildRequires:	net-snmp-devel
BuildRequires:	libgdbm-devel
BuildRequires:	perl-devel
BuildRequires:	glib2-devel
BuildRequires:	tcl tcl-devel
BuildRequires:	tkinter
BuildRequires:	tk tk-devel
Conflicts:	OpenIPMI
Requires(pre):	rpm-helper
Requires(post):	rpm-helper
# This rpm will replace OpenIPMI and OpenIPMI2 and IPMI
Obsoletes:	%{realname}
Obsoletes:	%{realname}2
Obsoletes:	%{oldlibname}
Obsoletes: 	IPMI
Provides:	IPMI
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

# Perl is usually installed in /usr/lib, not /usr/lib64 on 64-bit platforms.
#define perl_libdir %{_exec_prefix}/lib

%description 
This package contains a shared library implementation of IPMI and the
basic tools used with OpenIPMI.

%package devel
Summary:	Development files for OpenIPMI
Group:		Development/C
Requires:	%{name} = %{version}-%{release}
Obsoletes:	%{realname}-devel
Obsoletes:	%{realname}2-devel
Obsoletes:	%{oldlibname}-devel

%description devel
Contains additional files need for a developer to create applications
and/or middleware that depends on libOpenIPMI

%package -n perl-%{name}
Summary:	Perl interface for OpenIPMI
Group:		Development/Perl
Requires:	%{name} = %{version}-%{release}
Obsoletes:	%{name}-perl
Obsoletes:	perl-%{realname}2

%description -n perl-%{name}
A Perl interface for OpenIPMI.

%package -n python-%{name}
Summary:	Python interface for OpenIPMI
Group:		Development/Python
Requires:	%{name} = %{version}-%{release}
Obsoletes:	%{name}-python
Obsoletes:	python-%{realname}2

%description -n python-%{name}
A Python interface for OpenIPMI.

%package -n tcl-%{name}
Summary:	TCL interface for OpenIPMI
Group:		Development/Other
Requires:	%{name} = %{version}-%{release}
BuildRequires:	tcl-devel
Requires:	tcl

%description -n tcl-%{name}
A TCL interface for OpenIPMI.

%package gui
Summary:	GUI (in python) for OpenIPMI
Group:		System/Kernel and hardware
Requires:	python-%{name} = %{version}-%{release}
Requires:	wxPython >= 2.4.2
Requires:	wxPythonGTK
BuildRequires:	wxPythonGTK
Obsoletes:	%{realname}2-gui

%description gui
A GUI interface for OpenIPMI.  Written in python an requiring wxWidgets.

%package ui
Summary:	User Interface (ui)
Group:		System/Kernel and hardware
Requires:	%{name} = %{version}-%{release}
Obsoletes:	%{realname}2-ui

%description ui
This package contains a user interface

%package lanserv
Summary:	Emulates an IPMI network listener
Group:		System/Kernel and hardware
Requires:	%{name} = %{version}-%{release}
Obsoletes:	%{realname}2-lanserv

%description lanserv
This package contains a network IPMI listener.

%prep
%setup -q -n %{realname}-%{version}

%build
 
%configure2_5x	\
	--with-perlinstall=%{perl_vendorarch} \
	--with-pythoninstall=%{python_sitearch} \
	--with-glib12=no \
	--with-pythonusepthreads=yes \
	--with-perlusepthreads=yes

make

%install
rm -rf %{buildroot}
%makeinstall_std PYTHON_GUI_DIR=openipmigui
install -m755 ipmi.init -D %{buildroot}/%{_sysconfdir}/init.d/ipmi
install -m644 ipmi.sysconf -D %{buildroot}/%{_sysconfdir}/sysconfig/ipmi

%preun
%_preun_service ipmi

%postun
%if %mdkversion < 200900
/sbin/ldconfig
%endif
%_post_service ipmi

%if %mdkversion < 200900
%post -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%post -n tcl-%{name} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n tcl-%{name} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%post ui -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun ui -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%post lanserv -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun lanserv -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/libOpenIPMIcmdlang.so.*
%{_libdir}/libOpenIPMIcmdlang.la
%{_libdir}/libOpenIPMIglib.so.*
%{_libdir}/libOpenIPMIglib.la
%{_libdir}/libOpenIPMIposix.so.*
%{_libdir}/libOpenIPMIposix.la
%{_libdir}/libOpenIPMIpthread.so.*
%{_libdir}/libOpenIPMIpthread.la
%{_libdir}/libOpenIPMI.so.*
%{_libdir}/libOpenIPMI.la
%{_libdir}/libOpenIPMIutils.so.*
%{_libdir}/libOpenIPMIutils.la
%{_sysconfdir}/init.d/ipmi
%config(noreplace) %{_sysconfdir}/sysconfig/ipmi
%doc FAQ README README.Force
%doc README.MotorolaMXP

%files -n perl-%{name}
%defattr(-,root,root)
%{perl_vendorarch}/OpenIPMI.pm
%{perl_vendorarch}/auto/OpenIPMI
%doc swig/OpenIPMI.i swig/perl/sample swig/perl/ipmi_powerctl

%files -n python-%{name}
%defattr(-,root,root)
%{python_sitearch}/*OpenIPMI.*
%doc swig/OpenIPMI.i

%files -n tcl-%{name}
%defattr(-,root,root)
%{_libdir}/*OpenIPMItcl.so.*
%{_libdir}/*OpenIPMItcl.la

%files gui
%defattr(-,root,root)
%{python_sitearch}/openipmigui/*
%{_bindir}/openipmigui

%files devel
%defattr(-,root,root)
%{_includedir}/OpenIPMI
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/pkgconfig
%doc doc/IPMI.pdf

%files ui
%defattr(-,root,root)
%{_bindir}/ipmi_ui
%{_bindir}/ipmicmd
%{_bindir}/openipmicmd
%{_bindir}/ipmish
%{_bindir}/openipmish
%{_bindir}/solterm
%{_bindir}/rmcp_ping
%{_libdir}/libOpenIPMIui.so.*
%{_libdir}/libOpenIPMIui.la
%doc %{_mandir}/man1/ipmi_ui.1*
%doc %{_mandir}/man1/openipmicmd.1*
%doc %{_mandir}/man1/openipmish.1*
%doc %{_mandir}/man1/openipmigui.1*
%doc %{_mandir}/man1/solterm.1*
%doc %{_mandir}/man1/rmcp_ping.1*
%doc %{_mandir}/man7/ipmi_cmdlang.7*
%doc %{_mandir}/man7/openipmi_conparms.7*

%files lanserv
%defattr(-,root,root)
%{_bindir}/ipmilan
%{_libdir}/libIPMIlanserv.so.*
%{_libdir}/libIPMIlanserv.la
%doc %{_mandir}/man8/ipmilan.8*
