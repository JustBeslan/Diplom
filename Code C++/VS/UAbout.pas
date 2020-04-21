unit UAbout;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  StdCtrls, jpeg, ExtCtrls, Buttons, OleCtrls, SHDocVw,umain;

type
  TfAbout = class(TForm)
    Panel1: TPanel;
    SpeedButton1: TSpeedButton;
    WebBrowser1: TWebBrowser;
    procedure Button1Click(Sender: TObject);
    procedure SpeedButton7Click(Sender: TObject);
    procedure FormShow(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  fAbout: TfAbout;

implementation

{$R *.DFM}

procedure TfAbout.Button1Click(Sender: TObject);
begin
 fAbout.close;
end;

procedure TfAbout.SpeedButton7Click(Sender: TObject);
begin
 close;
end;

procedure TfAbout.FormShow(Sender: TObject);
begin
  fabout.WebBrowser1.Navigate(apl_path+'help\help.htm');
end;

end.
