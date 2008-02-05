%define realname OpenIPMI
%define name    openipmi
%define version 2.0.13
%define release %mkrel 1

#The lib naming in OpenIPMI 1.x
%define oldlibname %mklibname %realname 1

Name: 		%{name}
Summary: 	%{name} - Library interface to IPMI
Version: 	%{version}
Release: 	%{release}
License: 	LGPL
URL: 		http://openipmi.sourceforge.net
Group: 		System/Kernel and hardware
Source: 	%realname-%{version}.tar.bz2
BuildRequires:	swig >= 1.3
BuildRequires:	python-devel
BuildRequires:	popt-devel
BuildRequires:	ncurses-devel
BuildRequires:	net-snmp-devel
BuildRequires:	libgdbm-devel
BuildRequires:	perl-devel
BuildRequires:	glib2-devel
Conflicts:	OpenIPMI
Requires(pre):	rpm-helper
Requires(post): rpm-helper
Buildroot:      %{_tmppath}/%{name}-%{version}
# This rpm will replace OpenIPMI and OpenIPMI2
Obsoletes:	%{realname}
Obsoletes:	%{realname}2
Obsoletes:	%{oldlibname}


# Perl is usually installed in /usr/lib, not /usr/lib64 on 64-bit platforms.
#%define perl_libdir %{_exec_prefix}/lib

%description 
This package contains a shared library implementation of IPMI and the
basic tools used with OpenIPMI.

%package	devel
Summary:	Development files for OpenIPMI
Group:		Development/C
Requires:	%{name} = %{version} pkgconfig
Obsoletes:	%{realname}-devel
Obsoletes:	%{realname}2-devel
Obsoletes:	%{oldlibname}-devel


%description	devel
Contains additional files need for a developer to create applications
and/or middleware that depends on libOpenIPMI

%package -n	perl-%{name}
Summary:	Perl interface for OpenIPMI
Group:		Development/Perl
Requires:	%{name} = %{version}
Obsoletes:  %{name}-perl
Obsoletes:	perl-%{realname}2

%description -n perl-%{name}
A Perl interface for OpenIPMI.

%package -n	python-%{name}
Summary:	Python interface for OpenIPMI
Group:		Development/Python
Requires:	%{name} = %{version}
Obsoletes:  	%{name}-python
Obsoletes:	python-%{realname}2

%description -n python-%{name}
A Python interface for OpenIPMI.

%package	gui
Summary:	GUI (in python) for OpenIPMI
Group:		System/Kernel and hardware
Requires:	python-%{name} = %{version}-%{release}
Requires:	wxPython >= 2.4.2
Requires:	wxPythonGTK
BuildRequires:	wxPythonGTK
Obsoletes:	%{realname}2-gui

%description	gui
A GUI interface for OpenIPMI.  Written in python an requiring wxWidgets.

%package	ui
Summary:	User Interface (ui)
Group:		System/Kernel and hardware
Requires:	%{name} = %{version}
Obsoletes:	%{realname}2-ui

%description	ui
This package contains a user interface

%package	lanserv
Summary:	Emulates an IPMI network listener
Group:		System/Kernel and hardware
Requires:	%{name} = %{version}
Obsoletes:	%{realname}2-lanserv

%description	lanserv
This package contains a network IPMI listener.

###################################################
%prep
###################################################
%setup -q -n %realname-%{version}

###################################################
%build
###################################################
# Disabling the gui
%configure2_5x	--with-wxpython=yes \
		--with-perlinstall=%{perl_vendorarch} \
		--with-pythoninstall=%{python_sitearch} \
		--with-glib12=no
%make

###################################################
%install
###################################################
rm -rf %{buildroot}
%makeinstall_std
install -m755 ipmi.init -D %{buildroot}/%{_sysconfdir}/init.d/ipmi
install -m644 ipmi.sysconf -D %{buildroot}/%{_sysconfdir}/sysconfig/ipmi

###################################################
%preun
###################################################
%_preun_service ipmi

###################################################
%postun
###################################################
/sbin/ldconfig
%_post_service ipmi

%post -p /sbin/ldconfig

%post ui -p /sbin/ldconfig

%postun ui -p /sbin/ldconfig

%post lanserv -p /sbin/ldconfig

%postun lanserv
/sbin/ldconfig

%clean
rm -rf %{buildroot}

###################################################
%files
###################################################
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
%doc COPYING COPYING.LIB FAQ INSTALL README README.Force
%doc README.MotorolaMXP


###################################################
%files -n perl-%{name}
###################################################
%defattr(-,root,root)
%{perl_vendorarch}/OpenIPMI.pm
%{perl_vendorarch}/auto/OpenIPMI
%doc swig/OpenIPMI.i swig/perl/sample swig/perl/ipmi_powerctl

###################################################
%files -n python-%{name}
###################################################
%defattr(-,root,root)
%{python_sitearch}/*OpenIPMI.*
%doc swig/OpenIPMI.i
%exclude %{python_sitearch}/openipmigui

###################################################
%files gui
###################################################
%defattr(-,root,root)
%{python_sitearch}/openipmigui
%{_bindir}/openipmigui

###################################################
%files devel
###################################################
%defattr(-,root,root)
%{_includedir}/OpenIPMI
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/pkgconfig
%doc doc/IPMI.pdf

###################################################
%files ui
###################################################
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

###################################################
%files lanserv
###################################################
%defattr(-,root,root)
%{_bindir}/ipmilan
%{_libdir}/libIPMIlanserv.so.*
%{_libdir}/libIPMIlanserv.la
%doc %{_mandir}/man8/ipmilan.8*
