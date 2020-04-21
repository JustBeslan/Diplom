unit UsersList;

interface
uses Classes,windows;
procedure GetLocalUserList(ulist: TStrings);
implementation

///////////////////////////////////////////////////////////////////////////////
type NETSETUP_NAME_TYPE = (
                          NetSetupUnknown,
                          NetSetupMachine,
                          NetSetupWorkgroup,
                          NetSetupDomain,
                          NetSetupNonExistentDomain);

{$EXTERNALSYM NetUserEnum}
function NetUserEnum( servername    : LPWSTR;
level,
filter        : DWORD;
bufptr        : Pointer;
prefmaxlen    : DWORD;
entriesread,
totalentries,
resume_handle : LPDWORD    ) : DWORD; stdcall;
external 'NetApi32.dll' Name 'NetUserEnum';

{$EXTERNALSYM NetUserGetInfo}
function NetUserGetInfo(
         servername    : LPWSTR;
         username      : LPWSTR;
         level         : DWORD;
         bufptr        : Pointer) : DWORD; stdcall;
external 'NetApi32.dll' Name 'NetUserGetInfo';

{$EXTERNALSYM NetWkstaUserGetInfo}
function NetWkstaUserGetInfo(
         reserved    : LPTSTR;
         level         : DWORD;
         bufptr        : Pointer): DWORD; stdcall;
external 'NetApi32.dll' Name 'NetWkstaUserGetInfo';

{$EXTERNALSYM CreateMailslot}
function CreateMailslot(
         lpname    : WideChar; // for NT only; LPCTSTR - 4 W9x
         nMaxMessageSize: DWORD;
         lReadTimeout : DWORD;
         lpSecurityAttributes: Pointer): THandle; stdcall;
external 'NetApi32.dll' Name 'CreateMailslot';

{$EXTERNALSYM NetValidateName}
function NetValidateName(
         lpServer   : LPTSTR;
         lpName     : LPTSTR;
         lpAccount  : LPTSTR;
         lpPassword : LPTSTR;
         NameType   : NETSETUP_NAME_TYPE): DWORD; stdcall;
external 'NetApi32.dll' Name 'NetValidateName';
// {$EXTERNALSYM NetServerEnum}
//function NetServerEnum(
//         servername: LPCWSTR;
//         level         : DWORD;
//         bufptr        : Pointer): DWORD; stdcall;
//external 'NetApi32.dll' Name 'NetServerEnum';

function NetApiBufferFree( Buffer : Pointer{LPVOID} ) : DWORD; stdcall;

external 'NetApi32.dll' Name 'NetApiBufferFree';

//------------------------------------------------------------------------------
// ??? ???????????? ?????
//------------------------------------------------------------------------------
procedure GetLocalUserList(ulist: TStrings);
const

NERR_SUCCESS                     =  0;
FILTER_TEMP_DUPLICATE_ACCOUNT    =  $0001;
FILTER_NORMAL_ACCOUNT            =  $0002;
FILTER_PROXY_ACCOUNT             =  $0004;
FILTER_INTERDOMAIN_TRUST_ACCOUNT =  $0008;
FILTER_WORKSTATION_TRUST_ACCOUNT =  $0010;
FILTER_SERVER_TRUST_ACCOUNT      =  $0020;

type

TUSER_INFO_10 = record
usri10_name,
usri10_comment,
usri10_usr_comment,
usri10_full_name     : PWideChar;
end;
PUSER_INFO_10 = ^TUSER_INFO_10;

var

dwERead, dwETotal, dwRes, res : DWORD;
inf  : PUSER_INFO_10;
info : Pointer;
p    : PChar;
i    : Integer;
begin

if ulist=nil then
Exit;
ulist.Clear;


info  := nil;
dwRes := 0;
res := NetUserEnum( nil,10,FILTER_NORMAL_ACCOUNT,@info,65536,@dwERead,@dwETotal,@dwRes);
if  (info=nil) then Exit;
p := PChar(info);
for i:=0 to dwERead-1 do begin
inf := PUSER_INFO_10 ( p + i*SizeOf(TUSER_INFO_10) );
ulist.Add(WideCharToString( PWideChar((inf^).usri10_name) ));
end;
end;
end.
