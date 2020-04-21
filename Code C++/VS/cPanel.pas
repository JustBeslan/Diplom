unit cPanel;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  ExtCtrls;

type
  TCPanel = class(TPanel)
  private
    { Private declarations }
  protected
    { Protected declarations }
  public
      property canvas;
    { Public declarations }
  published
    { Published declarations }
  end;

procedure Register;

implementation

procedure Register;
begin
  RegisterComponents('Standard', [TCPanel]);
end;

end.
