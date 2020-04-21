unit UCapture;
        interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  Wave, StdCtrls, ExtCtrls, DXClass, DXSounds,uSpectr;

type
  TCaptureForm = class(TForm)
    StartButton: TButton;
    StopButton: TButton;
    FileNameEdit: TEdit;
    SizeLabel: TLabel;
    FormatBox: TComboBox;
    DriverBox: TComboBox;
    SaveDialog: TSaveDialog;
    BrowseButton: TButton;
    Image1: TImage;
    Image2: TImage;
    procedure StartButtonClick(Sender: TObject);
    procedure StopButtonClick(Sender: TObject);
    procedure FormCreate(Sender: TObject);
    procedure DriverBoxChange(Sender: TObject);
    procedure BrowseButtonClick(Sender: TObject);
    procedure FormClose(Sender: TObject; var Action: TCloseAction);
    procedure Image2MouseDown(Sender: TObject; Button: TMouseButton;
      Shift: TShiftState; X, Y: Integer);
    procedure Image2MouseUp(Sender: TObject; Button: TMouseButton;
      Shift: TShiftState; X, Y: Integer);
  private
    FCapture: TSoundCaptureStream;
    FWaveStream: TWaveStream;
    procedure CaptureFilledBuffer(Sender: TObject);
  end;

type
     comp=record re,im:real;end;

var
  CaptureForm:tform;
  Needformat,i,x,y:integer;
  bufc:array [1..512]of comp;

procedure FFTR(buf:array of comp);stdcall; external 'fftc.dll';

     implementation

{$R *.DFM}

procedure TCaptureForm.FormCreate(Sender: TObject);
var
  i: Integer;
begin
  for i:=0 to TSoundCaptureStream.Drivers.Count-1 do
    DriverBox.Items.Add(TSoundCaptureStream.Drivers[i].Description);
  DriverBox.ItemIndex := 0;
  DriverBoxChange(nil);
end;


procedure TCaptureForm.DriverBoxChange(Sender: TObject);
const
  ChannelText: array[1..2] of string = ('Mono', 'Stereo');
var
  i: Integer;
begin
  FCapture.Free;
  FCapture := TSoundCaptureStream.Create(nil);

  FormatBox.Items.Clear;
  for i:=0 to FCapture.SupportedFormats.Count-1 do
    with FCapture.SupportedFormats[i] do begin
      FormatBox.Items.Add(Format('%dHz %dbit %s', [SamplesPerSec, BitsPerSample, ChannelText[Channels]]));
      if FormatBox.Items[i]='22050Hz 8bit Mono' then Needformat:=i;
    end;


  FormatBox.ItemIndex := FormatBox.Items.Count-1;
end;

procedure TCaptureForm.StartButtonClick(Sender: TObject);
begin
  StopButtonClick(nil);
  try
    FWaveStream := TWaveFileStream.Create(FileNameEdit.Text, fmCreate);
    with FCapture.SupportedFormats[8] do
    FWaveStream.SetPCMFormat(22050, 8, 1);
    FWaveStream.Open(True);

    StartButton.Enabled := False;
    DriverBox.Enabled := False;
    FormatBox.Enabled := False;
    StopButton.Enabled := True;
    BrowseButton.Enabled := False;

    FileNameEdit.Color := clBtnFace;
    FileNameEdit.ReadOnly := True;

    FCapture.OnFilledBuffer := CaptureFilledBuffer;

    FCapture.CaptureFormat := 8;
    FCapture.Start;
  except
    StopButtonClick(nil);
    raise;
  end;
end;

procedure TCaptureForm.StopButtonClick(Sender: TObject);
begin
  if FCapture<>nil then FCapture.Stop;
  FWaveStream.Free; FWaveStream := nil;

  StartButton.Enabled := True;
  DriverBox.Enabled := True;
  FormatBox.Enabled := True;
  StopButton.Enabled := False;
  BrowseButton.Enabled := True;

  FileNameEdit.Color := clWindow;
  FileNameEdit.ReadOnly := False;
end;

procedure TCaptureForm.BrowseButtonClick(Sender: TObject);
begin
  if SaveDialog.Execute then
    FileNameEdit.Text := SaveDialog.FileName;
end;

procedure TCaptureForm.CaptureFilledBuffer(Sender: TObject);
var buf:array[0..512]of byte;
    bufI:array[0..512]of integer;
begin

  FWaveStream.CopyFrom(FCapture, FCapture.FilledSize);
  SizeLabel.Caption := Format('%d byte', [FWaveStream.Size]);
  FWaveStream.Seek(FWaveStream.Size-512,0);
  FWaveStream.read(buf,512);

        for i:=1 to 512 do
         begin
         bufc[I].Re:= buf[i]-128;
         bufc[I].Im:=0//left[i+x*step+begin_crop];
         end;
    fftr(bufc);
  Image1.Canvas.Brush.Color:=clwhite;
  Image1.Canvas.Rectangle(0,0,Image1.width,Image1.Height);
   for i:=128 to 256 do bufi[i-128]:=round((sqrt(sqr(bufc[I].Im)+sqr(bufc[I].re)))/3);
   for i:=1 to 128 do if bufi[i]>255 then bufi[i]:=255;

    for x:=1 to 4 do for y:=2 to 127 do
       bufi[y]:=round((bufi[y-1]+bufi[y]+bufi[y+1])/3);

   Image1.Canvas.MoveTo(0,128);
   for i:=1 to 128 do Image1.Canvas.LineTo(i,128-bufi[i]);
end;

procedure TCaptureForm.FormClose(Sender: TObject; var Action: TCloseAction);
begin
  StopButtonClick(nil);
  FCapture.Free;
  FCapture := nil;
  CaptureForm.Release;
  CaptureForm := nil;

end;

procedure TCaptureForm.Image2MouseDown(Sender: TObject;
  Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
begin
    FWaveStream := TWaveFileStream.Create(FileNameEdit.Text, fmCreate);
    with FCapture.SupportedFormats[8] do
    FWaveStream.SetPCMFormat(22050, 8, 1);
    FWaveStream.Open(True);

    FCapture.OnFilledBuffer := CaptureFilledBuffer;

    FCapture.CaptureFormat := 8;
    FCapture.Start;
end;

procedure TCaptureForm.Image2MouseUp(Sender: TObject; Button: TMouseButton;
  Shift: TShiftState; X, Y: Integer);

var spectr:array[1..128]of integer;
    i:integer;

begin
  if FCapture<>nil then FCapture.Stop;
  FWaveStream.Free; FWaveStream := nil;
  getspectr(FileNameEdit.text,spectr);
  Image1.Canvas.Brush.Color:=clwhite;
  Image1.Canvas.Rectangle(0,0,Image1.width,Image1.Height);
  Image1.Canvas.MoveTo(0,128);
  for i:=1 to 128 do Image1.Canvas.LineTo(i,128-spectr[i]);
end;

end.

