Summary:	Daemon that terminates users idle sessions
Summary(pl.UTF-8):	Demon który kończy nieaktywne sesje użytkowników
Name:		idled
Version:	1.16
Release:	13
License:	non-profit
Group:		Daemons
Source0:	http://www.darkwing.com/idled/download/%{name}-%{version}.tar.gz
# Source0-md5:	a633e9484acb904e1bf0ed43b8383033
Source1:	%{name}.init
Patch0:		%{name}-Makefile.patch
Patch1:		%{name}-man.patch
Patch2:		%{name}-config.patch
Patch3:		%{name}-utmp.patch
Patch4:		%{name}-yacc.patch
Patch5:		%{name}-O_NONBLOCK.patch
Patch6:		%{name}-malloc.patch
Patch7:		%{name}-freopen.patch
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post):	fileutils
Requires(post,preun):	/sbin/chkconfig
Requires:	/bin/mail
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Idled is a daemon that runs on a machine to keep an eye on current
users. If users have been idle for too long, or have been logged on
for too long, it will warn them and log them out appropriately.

%description -l pl.UTF-8
Idled jest demonem który pilnuje aktualnie zalogowanych użytkowników.
Jeśli użytkownik był nieaktywny przez odpowiednio długi czas, lub był
za długo zalogowany, idled ostrzeże go i odpowiednio zakończy sesję.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%build
%{__make} clean
%{__make} \
	CC="%{__cc}" \
	OPTFLAGS="%{rpmcflags} -DMAILMESSAGEFILE=\"%{_sysconfdir}/idled/logout.msg\""\
	LDFLAGS="%{rpmldflags}" \
	DEST="%{_sbindir}" \
	CFDEST="%{_sysconfdir}/idled" \
	MDEST="%{_mandir}" \
	LOGDEST="/var/log" \
	YACC="bison -y"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir}/idled,%{_mandir}/man{5,8},/var/log,/etc/rc.d/init.d}

install idled $RPM_BUILD_ROOT%{_sbindir}
install idled.conf.5 $RPM_BUILD_ROOT%{_mandir}/man5
install idled.8 $RPM_BUILD_ROOT%{_mandir}/man8
install idled.cf.template $RPM_BUILD_ROOT%{_sysconfdir}/idled/idled.conf.template

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/idled

touch $RPM_BUILD_ROOT/var/log/idled.log
touch $RPM_BUILD_ROOT%{_sysconfdir}/idled/logout.msg

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f /var/log/idled.log ]; then
	touch /var/log/idled.log
	chmod 640 /var/log/idled.log
fi
/sbin/chkconfig --add idled
%service idled restart

%preun
if [ "$1" = "0" ]; then
	%service idled stop
	/sbin/chkconfig --del idled
fi

%files
%defattr(644,root,root,755)
%doc README TODO CHANGES COPYRIGHT
%dir %{_sysconfdir}/idled
%{_sysconfdir}/idled/idled.conf.template
%{_sysconfdir}/idled/logout.msg
%attr(755,root,root) %{_sbindir}/idled
%attr(754,root,root) /etc/rc.d/init.d/idled
%{_mandir}/man[58]/idled*
%attr(640,root,root) %ghost /var/log/idled.log
