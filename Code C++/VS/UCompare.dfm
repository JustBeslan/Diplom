object Form2: TForm2
  Left = 197
  Top = 114
  BorderStyle = bsSingle
  Caption = 'Compare'
  ClientHeight = 356
  ClientWidth = 738
  Color = clBtnFace
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -11
  Font.Name = 'MS Sans Serif'
  Font.Style = []
  OldCreateOrder = False
  OnCreate = FormCreate
  PixelsPerInch = 96
  TextHeight = 13
  object Image1: TImage
    Left = 16
    Top = 56
    Width = 129
    Height = 128
  end
  object Image2: TImage
    Left = 16
    Top = 184
    Width = 137
    Height = 129
  end
  object Label1: TLabel
    Left = 80
    Top = 0
    Width = 32
    Height = 13
    Caption = 'Label1'
  end
  object Label2: TLabel
    Left = 80
    Top = 16
    Width = 32
    Height = 13
    Caption = 'Label2'
  end
  object Label3: TLabel
    Left = 304
    Top = 24
    Width = 41
    Height = 16
    Caption = 'Label3'
    Font.Charset = DEFAULT_CHARSET
    Font.Color = clLime
    Font.Height = -13
    Font.Name = 'MS Sans Serif'
    Font.Style = []
    ParentFont = False
  end
  object Label4: TLabel
    Left = 16
    Top = 48
    Width = 45
    Height = 13
    Caption = #1057#1087#1077#1082#1090#1088' 1'
    Font.Charset = DEFAULT_CHARSET
    Font.Color = clAqua
    Font.Height = -11
    Font.Name = 'MS Sans Serif'
    Font.Style = []
    ParentFont = False
    Transparent = True
  end
  object Label5: TLabel
    Left = 136
    Top = 48
    Width = 45
    Height = 13
    Caption = #1057#1087#1077#1082#1090#1088' 2'
    Font.Charset = DEFAULT_CHARSET
    Font.Color = clAqua
    Font.Height = -11
    Font.Name = 'MS Sans Serif'
    Font.Style = []
    ParentFont = False
    Transparent = True
  end
  object Label6: TLabel
    Left = 0
    Top = 184
    Width = 55
    Height = 13
    Caption = #1057#1088#1072#1074#1085#1077#1085#1080#1077
    Font.Charset = DEFAULT_CHARSET
    Font.Color = clAqua
    Font.Height = -11
    Font.Name = 'MS Sans Serif'
    Font.Style = []
    ParentFont = False
    Transparent = True
  end
  object Label7: TLabel
    Left = 296
    Top = 0
    Width = 55
    Height = 20
    Caption = 'Label7'
    Font.Charset = DEFAULT_CHARSET
    Font.Color = clLime
    Font.Height = -16
    Font.Name = 'MS Sans Serif'
    Font.Style = [fsBold]
    ParentFont = False
  end
  object Label8: TLabel
    Left = 80
    Top = 32
    Width = 32
    Height = 13
    Caption = 'Label8'
  end
  object BitBtn1: TBitBtn
    Left = 0
    Top = 312
    Width = 75
    Height = 25
    Caption = 'Close'
    TabOrder = 0
    OnClick = BitBtn1Click
  end
  object Button1: TButton
    Left = 0
    Top = 0
    Width = 75
    Height = 17
    Caption = 'File 1'
    TabOrder = 1
    OnClick = Button1Click
  end
  object Button2: TButton
    Left = 0
    Top = 16
    Width = 75
    Height = 17
    Caption = 'File 2'
    TabOrder = 2
    OnClick = Button2Click
  end
  object Button3: TButton
    Left = 0
    Top = 32
    Width = 75
    Height = 17
    Caption = 'compare'
    TabOrder = 3
    OnClick = Button3Click
  end
  object BitBtn2: TBitBtn
    Left = 184
    Top = 56
    Width = 105
    Height = 25
    Caption = 'BitBtn2'
    TabOrder = 4
    OnClick = BitBtn2Click
  end
  object Memo1: TMemo
    Left = 296
    Top = 48
    Width = 209
    Height = 297
    Lines.Strings = (
      'Memo1')
    ScrollBars = ssVertical
    TabOrder = 5
  end
  object BitBtn3: TBitBtn
    Left = 184
    Top = 88
    Width = 75
    Height = 25
    Caption = 'BitBtn3'
    TabOrder = 6
    OnClick = BitBtn3Click
  end
  object OpenDialog1: TOpenDialog
    FileName = 'D:\_Anton\_VoiceSec\test3.vsd'
    Filter = 'VSD`'#1096#1082#1080'|*.vsd'
    Left = 8
    Top = 200
  end
  object Timer1: TTimer
    Enabled = False
    Interval = 150
    OnTimer = Timer1Timer
    Left = 72
    Top = 200
  end
end
