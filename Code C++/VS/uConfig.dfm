object foConfig: TfoConfig
  Left = 219
  Top = 208
  BorderStyle = bsDialog
  Caption = 'foConfig'
  ClientHeight = 449
  ClientWidth = 688
  Color = clBtnFace
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -11
  Font.Name = 'MS Sans Serif'
  Font.Style = []
  OldCreateOrder = False
  PixelsPerInch = 96
  TextHeight = 13
  object PageControl1: TPageControl
    Left = 0
    Top = 0
    Width = 688
    Height = 449
    ActivePage = TabSheet1
    Align = alClient
    TabOrder = 0
    object TabSheet1: TTabSheet
      Caption = 'DB'
      object DBGrid1: TDBGrid
        Left = 0
        Top = 49
        Width = 680
        Height = 372
        Align = alClient
        DataSource = DataSource1
        TabOrder = 0
        TitleFont.Charset = DEFAULT_CHARSET
        TitleFont.Color = clWindowText
        TitleFont.Height = -11
        TitleFont.Name = 'MS Sans Serif'
        TitleFont.Style = []
      end
      object Panel1: TPanel
        Left = 0
        Top = 0
        Width = 680
        Height = 49
        Align = alTop
        TabOrder = 1
        object Edit1: TEdit
          Left = 0
          Top = 0
          Width = 681
          Height = 21
          TabOrder = 0
          Text = 'select * from registration'
        end
        object Button1: TButton
          Left = 0
          Top = 27
          Width = 75
          Height = 17
          Caption = 'Exec'
          TabOrder = 1
          OnClick = Button1Click
        end
      end
    end
    object TabSheet2: TTabSheet
      Caption = 'Настройки'
    end
  end
  object ADOQuery1: TADOQuery
    Connection = foMain.ADOConnection1
    CursorType = ctStatic
    Parameters = <>
    Prepared = True
    SQL.Strings = (
      'select * from registration')
    Left = 92
    Top = 72
  end
  object DataSource1: TDataSource
    DataSet = ADOQuery1
    Left = 124
    Top = 72
  end
end
