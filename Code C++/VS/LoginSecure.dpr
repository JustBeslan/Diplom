program LoginSecure;

uses
  Forms,
  uInMain in 'uInMain.pas' {foInMain};

{$R *.RES}

begin
  Application.Initialize;
  Application.CreateForm(TfoInMain, foInMain);
  Application.Run;
end.
