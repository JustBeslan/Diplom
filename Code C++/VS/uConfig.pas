unit uConfig;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  ComCtrls,umain, Db, StdCtrls, ExtCtrls, Grids, DBGrids, ADODB;

type
  TfoConfig = class(TForm)
    PageControl1: TPageControl;
    TabSheet1: TTabSheet;
    TabSheet2: TTabSheet;
    ADOQuery1: TADOQuery;
    DataSource1: TDataSource;
    DBGrid1: TDBGrid;
    Panel1: TPanel;
    Edit1: TEdit;
    Button1: TButton;
    procedure Button1Click(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  foConfig: TfoConfig;

implementation

{$R *.DFM}

procedure TfoConfig.Button1Click(Sender: TObject);
begin
   foconfig.ADOQuery1.Close;
   foconfig.ADOQuery1.SQL.Clear;
   foconfig.ADOQuery1.SQL.Add(edit1.text);
   runsql(foconfig.ADOQuery1,false);
end;

end.
