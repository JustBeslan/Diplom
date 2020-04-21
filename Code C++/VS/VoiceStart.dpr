program VoiceStart;

uses
  SvcMgr,
  uService in 'uService.pas' {Service1: TService};

{$R *.RES}

begin
  Application.Initialize;
  Application.CreateForm(TService1, Service1);
  Application.Run;
end.
