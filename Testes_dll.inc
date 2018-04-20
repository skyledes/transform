//<Vars>
Var
  MeasTime	  : real;       //Время измерения.
  IntStop         : integer;
  IntTact         : integer;	//Используются для отслеживания окончания выполнения ФК.
  AllPins	  : TLargeSet;	//AllPins - хранит список всех выводов микросхемы, кроме питания и земли.  
  ActiveBoard	  : integer;	//Номер первой из используемых ПИН-плат.
  DeviceNotReady  : boolean;	//Переменная для выхода в случае использования не подходящего  оборудования или его неработоспособности.
  DeltaBoard	  : integer;	//Для перепиновки. Смещение номера платы.
  DeltaH	  : integer;	//Для перепиновки. Смещение номера ПИНа.

  PWR             : TNamePower;
  PWROLD          : TNamePower;
  GND             : TNamePower;
  ComDCMPWR       : TEDCMComm;
  ComDCMGND       : TEDCMComm;
  First_Run	  : Boolean;	//Маркер проведения первой проверки в тесте.
  Last_Run	  : Integer;	//Переменная определяющая последний выполненный вектор.
  K		  : Integer;	//Используется как счетчик в цикле при последовательном обходе массива выводов.
//<Vars>


//<Const>
Label
  //метка для выхода из программы в случае использования на неподходящем/неисправном оборудовании
  ProgrammBrake;

Const
  //Делители для перевода величин
  Pico  = 1.0e-12;
  Nano  = 1.0e-9;
  Micro = 1.0e-6;
  Milli = 1.0e-3;
  Uno   = 1.0e-0;
  NULL = 0.00;
  dU = 0.25;
  IConnect = 60.0e-9;
  TimeUSB = 10;
  //Начальные значения различных напряжений, могут изменяться в процессе выполнения программы
  Upwr_0 : Real	= 0;
  Ugnd_0 : Real	= 0;
  DRH_0	 : Real	= 0;
  DRL_0	 : Real	= 0;
  DRH1_0 : Real	= 0;
  DRL1_0 : Real	= 0;

  FullText : PChar = '';	//Определяет дополняемый текст информационного сообщения
  TesNum   : Integer = 138;	// Номер тестера

  IMSNumber    : Integer = 0;			//номер проверяемой ИС, для модуля статистики
  TestNumber   : Integer = 0;			//номер теста, для модуля статистики
  ShortName    : String  = '';			//строка с коротким именем теста
  PowerComment : String  = '';			//строка с напряжением питания
  PNum	       : String  = '';			//строка с именем и номером проверяемого вывода
  WTFVar       : Real    = 0.0;			//костыль для функций
  ConnPins     : TLargeSet = [];		//выводы подключаемые в функциях UO/ILI, при необходимости перезадаются перед вызовом функции
//<Const>

//<Dllfunc>
Procedure Initialise(FName, PPVersion, MadeDate, DesignerName : String; testerNumber : integer; Var IMSNumber : integer); stdcall; external 'PrintResult.dll' name 'Init';
Procedure Header(FName : String; Var IMSNumber : integer; DebugMode : boolean); stdcall; external 'PrintResult.dll' name 'HeadPrint';
Procedure SaveResult(FName, TName : String; Var PowComm : String; Var PNum : String; Var ShTestName : String; PinName : String; PinNum : integer; UccValue : real; Var Value : real; var LBound : real; var UBound : real; dim, tin : real; Var IMSNumber : integer; Var testNum : integer); stdcall; external 'PrintResult.dll' name 'Print1';	
Procedure Repin(PinS, Adap60 : boolean; TesterNumber : integer; Var BoardChange : integer; Var PinChange : integer; Var InfoText : String; Adapter, Kontakt, Jumpers, Pin2 : String); stdcall; external 'Repin.dll' name 'Repin';
//<Dllfunc>

//<Basefunc>

//<Deltaproc>
//функция изменения значений пинов
Procedure DeltaProc(Var DeltaSet : TLargeSet; Displacement : Integer);
  Var
    TempSet : TLargeSet;
    I : integer;
  Begin
    TempSet := [];
    for I := 1 to 256 do
      begin
        if (I in DeltaSet) then
	  begin
	    exclude(DeltaSet, I);
	    include(TempSet, I + Displacement);
	  end;
      end;
    deltaSet := TempSet;
  End;
//<Deltaproc>

//<ConnectPinN>
//Подключение пинов с учетом перепиновки
Procedure ConnectPinN(Pin : Integer; Conn : TbitComm);
  Begin
    ConnectPin(Pin + DeltaH, Conn);
    DelayMS(TimeUSB);
  End;
//<ConnectPinN>

//<ConnectPinsN>
//Подключение пинов с учетом перепиновки
Procedure ConnectPinsN(Var DeltaSet : TLargeSet; Conn : TbitComm);
  Var
    Temp : TLargeSet;
    i : Integer;
  Begin
    Temp := [];
    for i := 1 to 256 do
      begin
        if (i in DeltaSet) then
	  begin
	    include(Temp,i + DeltaH);
	  end;
      end;
      ConnectPins(Temp, Conn);
      DelayMS(TimeUSB);
  End;
//<ConnectPinsN>

//<ConfChnl>
Procedure ConfChnl(ch : Integer; mode : TChMode; state : TChState);
  Begin
    conf_chnl_hand(ch + DeltaH, mode, state);
    DelayMS(TimeUSB);
  End;
//<ConfChnl>

//<ConfChnlN>
Procedure ConfChnlN(Var chs : TLargeSet; mode : TChMode; state : TChState);
  Var
    Temp : TLargeSet;
    i : Integer;
  Begin
    Temp := [];
    for i := 1 to 256 do
      begin
        if (i in chs) then
	  begin
	    include(Temp, i + DeltaH);
	  end;
      end;
    conf_levels_hand(Temp, mode, state);
    DelayMS(TimeUSB);
  End;
//<ConfChnlN>

//<Printrestu>
//Распечатка результа в единицах ТУ
//        PrintResTU(TestName, PinNum, Upwr, Value, LowerBound, UpperBound, Dim);
Procedure PrintResTU(TestName : PChar; PinNum : integer; Upwr, Value, LowerBound, UpperBound, Dim: Real);
  Begin
    if PinNum <> -1 Then
      SaveResult(FileName, TestName, PowerComment, PNum, ShortName, NamePin[PinNum], PinNum, Upwr, Value, LowerBound, UpperBound, Dim, Tin, IMSNumber, TestNumber);
    else
      SaveResult(FileName, TestName, PowerComment, PNum, ShortName, '', PinNum, Upwr, Value, LowerBound, UpperBound, Dim, Tin, IMSNumber, TestNumber);
    PrintResult(ShortName, PNum, Value, LowerBound, UpperBound, PowerComment);
  End;
//<Printrestu>

//<Updown>
//Плавное изменение питания
//необходима для уменьшения выбросов при изменении напряжения питания и драйверов
//UPWR,UGND,DRH,DRL,DRH1,DRL1-конечные напряжения dU-Шаг с которым стремиться к новым напряжениям
	//UpDown(Boards, Upwr, Ugnd, DRH, DRL, DRH1, DRL1, dU);
Procedure UpDown(Var Boards : TLargeSet; Upwr, Ugnd, DRH, DRL, DRH1, DRL1, dU : Real);
  Var
    J  : Integer;
    delta, deltaP, deltaG, deltaDRH, deltaDRL, deltaDRH1, deltaDRL1 : Real;//Амплитуды изменения напржений.
  Begin
    //находим разницы между текущими и требуемыми уровнями111
    deltaP    := Upwr - Upwr_0;
    deltaG    := Ugnd - Ugnd_0;
    deltaDRH  := DRH  - DRH_0;
    deltaDRL  := DRL  - DRL_0;
    deltaDRH1 := DRH1 - DRH1_0;
    deltaDRL1 := DRL1 - DRL1_0;
    //определяем максимальный перепад напряжения
    if abs(deltaP) < abs(deltaG) then
      delta := abs(deltaG);
    else
      delta := abs(deltaP);

    if delta < abs(deltaDRH) then
      delta := abs(deltaDRH);

    if delta < abs(deltaDRL) then
      delta := abs(deltaDRL);

    if delta < abs(deltaDRH1) then
      delta := abs(deltaDRH1);

    if delta < abs(deltaDRL1) then
      delta := abs(deltaDRL1);

    //рассчитываем необходимое число шагов
    J := trunc(delta/dU);
    
    //при максимальном перепаде напряжения больше шага
    if J > 0 then
      begin
        //рассчитываем необходимое изменение напряжения за 1 итерацию
        deltaP    := deltaP    / J;		
	deltaG    := deltaG    / J;		
	deltaDRH  := deltaDRH  / J;		
	deltaDRL  := deltaDRL  / J;		
	deltaDRH1 := deltaDRH1 / J;		
	deltaDRL1 := deltaDRL1 / J;		
	//запускаем итерационный цикл изменения напряжений
	for K:=1 to J do
	  begin				
	    //вычисляем новые значения напряжений
	    Upwr_0 := Upwr_0 + deltaP;
	    Ugnd_0 := Ugnd_0 + deltaG;
	    DRH_0  := DRH_0  + deltaDRH;
	    DRL_0  := DRL_0  + deltaDRL;
	    DRH1_0 := DRH1_0 + deltaDRH1;
	    DRL1_0 := DRL1_0 + deltaDRL1;
	    //задаем питание источников
	    SetPowerU(PWR, Upwr_0);	
	    SetPowerU(GND, Ugnd_0);
	    //задаем уровни напряжений на драйверах
	    LoadDACPinsLevels(Boards, DRH_0, DRL_0, (Upwr_0 - Ugnd_0)/2+1, (Upwr_0 - Ugnd_0)/2-1, DRH1_0, DRL1_0);//Установка новых уровней U.
	    DelayMS(TimeUSB);
	  end;
      end;

    //после выхода из цикла или при максимальном изменении питания меньше шага
    //окончательно задаем требуемые уровни напряжений на драйверах
    LoadDACPinsLevels(Boards, DRH, DRL, (Upwr - Ugnd)/2+1, (Upwr - Ugnd)/2-1, DRH1, DRL1);
    //и на источниках
    SetPowerU(PWR, Upwr);
    SetPowerU(GND, Ugnd);
    DelayMS(TimeUSB);

    //записываем текущие значения напряжений в переменные для использования в дальнейшем
    Upwr_0 := Upwr;
    Ugnd_0 := Ugnd;
    DRH_0  := DRH ;
    DRL_0  := DRL ;
    DRH1_0 := DRH1;
    DRL1_0 := DRL1;
  End;
//<Updown>

//<Unconnectalll>
//Плавное отключение
// Необходима для избежания скачков тока и напряжения в системе при отключении.
Procedure UnConnectAlll(us0, us1 : Integer);
  Var
    S: Integer;
  Begin
    //Отключение режима активной нагрузки для всех плат
    TERminationMode ([1..16], TermOFF, 0.0, 0.0, 0.0);
    DelayMs(TimeUSB);
    
    //Отключение второго набора уровня драйверов для всех выводов
    ConfChnlN(AllPins, DNRZ, []);
    DelayMs(TimeUSB);

    //Задание на всех пинах порта USER_0 нулей.
    PRGUser(UserPort_0, us0);
    DelayMs(TimeUSB);

    //Задание на всех пинах порта USER_1 нулей.
    PRGUser(UserPort_1, us1);
    DelayMs(TimeUSB);
	
    //Вызов функции UpDown для плавного понижения напряжения на питании и драйверах.
    UpDown(BoardList, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25);
	
    //маскируем все пины для 16 плат
    for K := 0 to 15 do
      begin
	SendPat(K, 0, 65535);
	DelayMs(TimeUSB);
      end;

    //отключаем все пины в воздух
    ConnectPins([1..256], []);
    DelayMs(TimeUSB);

    //отключаем все источники для всех плат SVPN
    for S := 1 to 4 do
      begin
        ActivateSVPN(S);
        DelayMs(TimeUSB);

        SetDCM(0.0, R8, 1.0e-6, DCM_1);
        DelayMs(TimeUSB);
		
	ConnectDCM(DCM_Off);
	DelayMs(TimeUSB);
		
	SetPower(pVCC, 0.0, 1.0e-6, Source_off);
	DelayMs(TimeUSB);
		
	SetPower(pVDD, 0.0, 1.0e-6, Source_off);
	DelayMs(TimeUSB);
		
	SetPower(pVEE, 0.0, 1.0e-6, Source_off);
	DelayMs(TimeUSB);
      end;

    //оригинальная функция "отключения всего" от ФОРМ-а
    UnConnectAll;
    DelayMs(TimeUSB);
  End;
//<Unconnectalll>

//<Raportprint>
//процедура распечатки имени разработчика, даты отработки и версии ПП
Procedure RaportPrint(MeasTime : real);
  Begin
    SaveResult(FileName, 'Время измерения, c', PowerComment, PNum, ShortName, '', -1, NULL, MeasTime, MeasTime, MeasTime, Uno, Tin, IMSNumber, TestNumber);
    PrintResult('Время измерения, c', '', MeasTime, MeasTime, MeasTime, '');
    PrintResult(Data,'', 0, 0, 0, '');
    PrintResult('Разработчик ПП:', '', 0, 0, 0,'');
    PrintResult(Raz, '', 0, 0, 0, '');
    PrintResult(Ver, '', 0, 0, 0, '');
    PrintResult(TU, '', 0, 0, 0, '');
  End;
//<Raportprint>

//<Basefunc>

//<Pinchangedll>
//функция перепиновки с использованием внешних библиотек
Procedure PinChangeDll();
  Begin
    //получение номера тестера
    if DEBUG = false then
      TesNum := GetTesterNumber // Заводской номер Тестера
    else
      TesNum := StrToInt (InputBox('Введите номер тестера'));

    //перепиновка, PinS, Adap60 - bool, DeltaBoard, DeltaH - переменные, изменяемые функцией
    //FullText - переменная для дальнейшего вывода текста сообщения
    //Adap, KU, Jamper, Pin2 - переменные с информацией о применяемой оснастке
    Repin(RepinN, Adap60, TesNum, DeltaBoard, DeltaH, FullText, Adap, KU, Jumper, LastBoard);

    //задание имен файлов в зависимости от номера используемой H-платы
    if DeltaBoard = 2 then
      StrConcat(FileName, '_1029_1033');

    if DeltaBoard = 4 then
      StrConcat(FileName, '_135_1053');
 
    if DeltaBoard = 6 then
      StrConcat(FileName, '_adap60');
  
    if DeltaBoard = 9 then
      StrConcat(FileName, '_148');
  
    //вывод ошибки если программа не проверяется на данном тестере
    if DeltaBoard = -1 then
      begin
        ErrorBox(FullText, 'Ошибка');
        DeviceNotReady := true;
      end
    else
      begin
      //перепиновка массивов используемых пин-плат, входных и выходных пинов
      //DeltaProc(DeltaSet, Displacement);
        DeltaProc(BoardList, DeltaBoard);

        ActiveBoard := DeltaBoard + 1;	

        //вывод сообщения о подключении оснастки
        InfoBox(FullText, FileName);
        DeviceNotReady := false;
      end;
  End;
//<Pinchangedll>

//<Contact>
//5
//Procedure Contact(Var MeasPin : TLargeSet; UDCM, IDCM, LBound, UBound : Real);
//AllPins; Список контролируемых выводов
//-2.0; Напряжение DCM, В
//10.0e-6; Ток DCM, А
//-1.5; Нижняя граница, В
//-0.3; Верхняя граница, В
//Контроль контактирования и КЗ
//Не ТУ
//Каждый вывод ИМС соединён с GND через диод. Подача отрицательного напряжения открывает диод, меряется падение U на диоде (LB<U<UB).
//В случае U > UpperBound видим КЗ (диод пробит, сопротивление замкнутого контакта 0).
//В случае U < LowerBound видим обрыв - вывод тестера не подключен к исследуемому выводу ИМС.
//        Contact( MeasPin, UDCM, IDCM, LBound, UBound, NamePWR);
Procedure Contact(Var MeasPin : TLargeSet; UDCM, IDCM, LBound, UBound : Real);
  Var
    Ucont : Real;
  Begin
    
    //устанавливаем нужный уровень питания и тока на DCM
    SetDCM(UDCM, RAuto, IDCM, DCM_Auto);             
    DelayMS(TimeUSB);

    //подключение DCM к источнику питания
    ConnectDCM(ComDCMPwr);                 
    DelayMs(TimeMeasU);                    

    //измерение напряжения
    Ucont := OnlyMeasDCMVoltage(ADCRange_AUTO); 

    //при браке выводим результат на экран
    if (Ucont > UBound) or (Ucont < LBound) then
    //PrintResTU (         TestName,   PinNum, Upwr, Value, LBound, UBound, Dim);
      PrintResTU ('Контактирование', NumOfPin, NULL, Ucont, LBound, UBound, Uno);
    //иначе вывод результата только во внешний рапорт
    else
      SaveResult(FileName, 'Контактирование', PowerComment, PNum, ShortName, NamePin[NumOfPin], NumOfPin, NULL, UCont, LBound, UBound, Uno, Tin, IMSNumber, TestNumber);

    //подключаем DCM к измерительной шине
    ConnectDCM(DCM_To_Pins);
    DelayMs(TimeUSB);
    
    //цикл по всем выводам
    for K := 1 to NumOfPin do
      begin
        //пропуск итерации если вывод не в списке измеряемых
        if not(K in MeasPin) then continue;

	//подключение вывода к DCM
        ConnectPinN(K, [Pin_To_DCM]);

	//измерение падения напряжения
        Ucont:= OnlyMeasDCMVoltage(ADCRange_AUTO);

	//отключаем вывод в воздух
        ConnectPinN(K, []);

	//при браке выводим результат на экран
        if (Ucont > UBound) or (Ucont < LBound) then
        //PrintResTU(         TestName, PinNum, Upwr, Value, LBound, UBound, Dim);
	  PrintResTU('Контактирование',      K, UDCM, Ucont, LBound, UBound, Uno);
	//иначе печатаем результат только во внешний рапорт
	else
          SaveResult(FileName, 'Контактирование', PowerComment, PNum, ShortName, NamePin[K], K, NULL, UCont, LBound, UBound, Uno, Tin, IMSNumber, TestNumber);
      end;

    SetDCM(NULL, RAuto, IConnect, DCM_1);
    DelayMS(TimeUSB);

    ConnectDCM(DCM_Off);
    DelayMS(TimeUSB);

  End;
//<Contact>

//<Uo>
//15
//Function UO(Var MPins : TLargeSet; Upwr, Ugnd, DRL, DRH, DRL1, DRH1, ILimDCM, UDCM, LBound, UBound : Real; StartFK : Integer; Var  StopFK : TVectors; TestName : String; Mode : Integer) : Real;
//OutPins; Список проверяемых выводов
//5.0; Напряжение питания, В
//0.0; Смещение земли, В
//0.4; Напряжение низкого уровня, В
//4.5; Напряжение высокого уровня, В
//0.0; Доп.напряжение низкого уровня, В
//0.0; Доп.напряжение высокого уровня, В
//1.3e-3; Выходной ток, А
//2.5; Выходное напряжение измерителя, В
//0.8; Нижняя граница, В
//4.0; Верхняя граница, В
//0000; Начальный вектор FK
//VectorUOH; Конечный вектор FK
//1.Напр.выс.ур.UOH,B?1. Напряжение высокого уровня UOH, В; Имя теста
//0000; Установка режима (установочные тесты, при наличии никакие дополнительные выводы не подключаются (0 - нет, 1 - есть), 2 разряд - подключение DCM (0 - до пинов, 1 - после), 3 разряд - экстраполяция (0 - нет, 1 - есть), 4 разряд - отключение выводов в конце функции (0 - не отключать, 1 - отключить), 5 разряд - режим печати (0 - печатать результат измерения, 1 - нет) 
//Измерение напряжения по выходу
//Значения mode: 
//1 разряд - установочные тесты, при наличии никакие дополнительные выводы не подключаются (0 - нет, 1 - есть)
//2 разряд - подключение DCM (0 - до пинов, 1 - после)
//3 разряд - экстраполяция (0 - нет, 1 - есть)
//4 разряд - отключение выводов в конце функции (0 - не отключать, 1 - отключить)
//5 разряд - режим печати (0 - печатать результат измерения, 1 - нет)
       //UO(MPins, Upwr, Ugnd, DRL, DRH, DRL1, DRH1, ILimDCM, UDCM, LBound, UBound, StartFK, StopFK, TestName, Mode);
Function UO(Var MPins : TLargeSet; Upwr, Ugnd, DRL, DRH, DRL1, DRH1, ILimDCM, UDCM, LBound, UBound : Real; StartFK : Integer;
	     Var  StopFK : TVectors; TestName : String; Mode : Integer) : Real;
  Var
    Corr, Upwr_real, U : Real;
  Begin
    
    //при необходимости смещаем все уровни с учетом уровня земли
    if not VEEON then
      Ugnd := 0.0;
    Upwr	:= Upwr + Ugnd;
    UDCM	:= UDCM + Ugnd;
    DRL		:= DRL  + Ugnd;
    DRH		:= DRH  + Ugnd;
    DRL1	:= DRL1 + Ugnd;
    DRH1	:= DRH1 + Ugnd;
    Corr	:= NULL;

    //устанавливаем изначальный уровень напряжения и тока на DCM и отключаем его 
    SetDCM(UDCM, RAuto, IConnect, DCM_1);
    DelayMS(TimeUSB);

    ConnectDCM(DCM_Off);
    DelayMS(TimeUSB);

    //наличие установочных тестов
    if (mode and !0001) = 0 then
      begin
      //задаем нулевые уровни напряжения на источниках и драйверах
      //UpDown(   Boards, Upwr, Ugnd,  DRH,  DRL, DRH1, DRL1, dU);
	UpDown(BoardList, NULL, NULL, NULL, NULL, NULL, NULL, dU);
	
	//отключаем все пины
	ConnectPins([1..256], []);
	DelayMS(TimeUSB);
	
	//устанавливаем 0 на всех каналах всех плат
	for K := 0 to 15 do
	  begin
	    SendPat(K, 0, 0);
	    DelayMS(TimeUSB);
	  end;
        ConnectPinsN(ConnPins, [Pin_To_Drivers]);
      end;


  //задаем нужные уровни напряжений
  //UpDown(   Boards, Upwr, Ugnd, DRH, DRL, DRH1, DRL1, dU);
    UpDown(BoardList, Upwr, Ugnd, DRH, DRL, DRH1, DRL1, dU);
  
    //при использовании смещенной земли измеряем погрешность ее задания
    if VEEON then
      begin
	//подключаем DCM к источнику, имитирующему землю
	ConnectDCM(ComDCMGND);
	DelayMS(TimeMeasU);
	
	//измеряем реальное значение заданного напряжения
	Corr := -1.0 * OnlyMeasDCMVoltage(ADCRange_AUTO);

	//отключаем DCM
	ConnectDCM(DCM_Off);
	DelayMS(TimeUSB);
      end;
    
    //при необходимости экстраполяции измеряем погрешность источника питания
    if (mode and !0100) <> 0 then
      begin
        //подключаем DCM к источнику
        ConnectDCM(ComDCMPWR);
	DelayMS(TimeMeasU);

	//устанавливаем нужные уровни напряжения и тока на DCM
        if Upwr > 7.5 then
          SetDCM(UDCM, R20_42, ILimDCM, DCM_Auto);
        else
          SetDCM(UDCM, R8, ILimDCM, DCM_Auto);
        DelayMs(TimeMeasU);

	//измеряем реальное напряжение на источнике
	Upwr_real := (OnlyMeasDCMVoltage(ADCRange_AUTO) + OnlyMeasDCMVoltage(ADCRange_AUTO) + OnlyMeasDCMVoltage(ADCRange_AUTO))/3;
	if DEBUG then
          InfoBox(Upwr_real,'');
	//находим погрешность с заданным значением питания
	Upwr_real := Upwr - Upwr_real;
	//добавляем полученную погрешность в коррекцию
	Corr := Corr + Upwr_real;

	//отключаем DCM
	ConnectDCM(DCM_Off);
	DelayMS(TimeUSB);
      end;

    //проверка необходимости подключать DCM после подключения пинов
    if (mode and !0010) = 0 then
      begin
        ConnectDCM(DCM_To_Pins);
        DelayMS(TimeUSB);
        if not ILimDCM > 1.0e-3 then
        begin
          SetDCM(UDCM, RAuto, ILimDCM, DCM_Auto);
          DelayMS(TimeUSB);
        end;
      end;

    //сбрасываем переменные отвечающие за первый запуск ФК
    First_Run:= True;
    Last_Run := 1;

    //цикл по всем выводам ИС
    for K := 1 to NumOfPin do
      begin
        //пропускаем вывод если он не в списке измеряемых
        if not(K in MPins) then
	  continue;
   
        //если это первый запуск или номер вектора проверки не совпадает с предыдущим запуском повторно запускаем ФК
        if StopFK[Last_Run]<>StopFK[K] or First_Run then
          begin
            start_beg_hand(StartFK, StopFK[K], 1, 0, 1);
            repeat intStop := check_stop(intTact);
            DelayCompMks(100);
            until intStop <> 0;
            First_Run := False;
          end;
      
        //сохраняем номер последнего проверенного вывода
        Last_Run := K;
      
        //подключаем текущий вывод к измерителю
        ConnectPinN(K, [Pin_To_DCM]);

        //при необходимости подключаем DCM к измерительной шине
   
        if (mode and !0010) <> 0 then
          begin
	    ConnectDCM(DCM_To_Pins);
	    DelayMS(TimeUSB);
	  end;
      
        //устанавливаем нужные уровни напряжения и тока на DCM
        if Upwr > 7.5 then
          SetDCM(UDCM, R20_42, ILimDCM, DCM_Auto);
        else
          SetDCM(UDCM, R8, ILimDCM, DCM_Auto);
        DelayMs(TimeMeasU);
      
        //собственно измерение напряжения
        U := OnlyMeasDCMVoltage(ADCRange_AUTO) + Corr;
        DelayMs(TimeUSB);

        //при необходимости понижаем ток DCM перед отключением
        if ILimDCM > 1.0e-3 then
          begin
	    SetDCM(UDCM, RAuto, Iconnect, DCM_1);
	    DelayMs(TimeUSB);
	  end;

        //если вывод двунаправленный или выбран режим подключения выходных пинов
        //подключаем ножку к драйверам
        if (K in ConnPins) then 
	  ConnectPinN(K, [Pin_To_Drivers]);
	else
          //в противном случае отключаем ее в воздух 
	  ConnectPinN(K, []);
	  
        //при необходимости отключаем DCM от измерительной шины
        if (mode and !0010) <> 0 then
          begin
            ConnectDCM(DCM_Off);
	    DelayMS(TimeUSB);
          end;

        //если не задан режим "не печати" выводим полученный результат
        if (mode and !10000) = 0 then
        //PrintResTU(TestName, PinNum,      Upwr, Value, LBound, UBound, Dim);
          PrintResTU(TestName,      K, Upwr-Ugnd,     U, LBound, UBound, Uno);

      end;
    
    //отключаем DCM от измерительной шины
    ConnectDCM(DCM_Off);
    DelayMS(TimeUSB);

    if (mode and !1000) <> 0 then
      begin
      //задаем нулевые уровни напряжения на источниках и драйверах
      //UpDown(   Boards, Upwr, Ugnd,  DRH,  DRL, DRH1, DRL1, dU);
	UpDown(BoardList, NULL, NULL, NULL, NULL, NULL, NULL, dU);
        
	ConnectPinsN(ConnPins, []);
      end;
    //возвращаем из функции измеренное значение
    result := U;

  End;
//<Uo>

//<Ili>
//15
//Function ILI(Var MeasPin : TLargeSet; Upwr, Ugnd, UDCM, DRL, DRH, DRL1, DRH1, LBound, UBound, Dim : Real; StartFK : Integer; Var  StopFK : TVectors; TestName : String; mode : Integer) : Real;
//InPins; Список проверяемых выводов
//5.0; Напряжение питания, В
//0.0; Смещение земли, В
//5.0; Выходное напряжение измерителя, В
//0.4; Напряжение низкого уровня, В
//4.5; Напряжение высокого уровня, В
//0.0; Доп.напряжение низкого уровня, В
//0.0; Доп.напряжение высокого уровня, В
//-12.0e-9; Нижняя граница, А
//1.0e-6; Верхняя граница, А
//micro; Делитель (Uno: e-0, milli: e-3, micro: e-6, nano: e-9, pico: e-12)
//0000; Начальный вектор FK
//VectorIIL; Конечный вектор FK
//3.Ток.низк.ур.IIL,мкА?3. Ток низкого уровня IIL, мкА; Имя теста
//0000; Установка режима (1 разряд - установочные тесты, при наличии никакие выводы не подключаются (0 - нет, 1 - есть), 2 разряд - подключение DCM (0 - до пинов, 1 - после), 3 разряд - не используется, 4 разряд - отключение выводов в конце функции (0 - не отключать, 1 - отключить), 5 разряд - режим печати (0 - печатать результат измерения, 1 - нет) 
//Измерение тока утечки
//Значения mode: 1 разряд - установочные тесты, при наличии никакие выводы не подключаются (0 - нет, 1 - есть)
//2 разряд - подключение DCM (0 - до пинов, 1 - после)
//3 разряд - не используется
//4 разряд - подключение выходных пинов (0 - отключены, 1 - подключены к драйверам)
//5 разряд - режим печати (0 - печатать результат измерения, 1 - нет)
//       ILI( MeasPin, Upwr, Ugnd, UDCM, DRL, DRH, DRL1, DRH1, LBound, UBound, Dim, StartFK, StopFK, TestName, mode);
Function ILI(Var MeasPin : TLargeSet; Upwr, Ugnd, UDCM, DRL, DRH, DRL1, DRH1, LBound, UBound, Dim : Real; StartFK : Integer;
              Var  StopFK : TVectors; TestName : String; mode : Integer) : Real;
  Var
    I : Real;
    IDCM : Real;
  Begin
    //находим максимальную границу для определения ограничения по току источника-измерителя
    if ABS(LBound) > ABS(UBound) then 
      IDCM := ABS(LBound) 
    else 
      IDCM := ABS(UBound);
    
    //устанавливаем итоговую границу с запасом в 50% или 1.79 мкА при малых токах
    if IDCM < 1.5e-6 then 
      IDCM := 1.79e-6 
    else 
      IDCM := IDCM * 1.5;

    //убеждаемся, что при выключенном режиме смещенной земли смещение равно 0
    if VEEON <> true then 
      Ugnd := 0.0;
    
    //корректируем значения напряжений с учетом смещенной земли
    Upwr := Upwr + Ugnd;
    DRL  := DRL  + Ugnd;
    DRH  := DRH  + Ugnd;
    DRL1 := DRL1 + Ugnd;
    DRH1 := DRH1 + Ugnd;
    UDCM := UDCM + Ugnd;
   
    if (mode and !0001) = 0 then
      begin
      //задаем нулевые уровни напряжения на источниках и драйверах
      //UpDown(   Boards, Upwr, Ugnd,  DRH,  DRL, DRH1, DRL1, dU);
        UpDown(BoardList, NULL, NULL, NULL, NULL, NULL, NULL, dU);

        //подключаем к драйверам входные пины
        ConnectPinsN(ConnPins, [Pin_To_Drivers]);
      end;

    //при необходимости уменьшаем ток DCM на момент коммутации
    if IDCM > 1.0e-3 then
      SetDCM(UDCM, RAuto, IConnect, DCM_1);
    else
      SetDCM(UDCM, RAuto, IDCM, DCM_Auto);
    DelayMS(TimeUSB);

    //подключаем DCM к измерительной шине, если не выбрано обратное
    if (mode and !0010) = 0 then
      ConnectDCM(DCM_To_Pins);
    else
      ConnectDCM(DCM_Off);
    DelayMS(TimeUSB);

  //устанавливаем нужные уровни на источниках и драйверах
  //UpDown(   Boards, Upwr, Ugnd, DRH, DRL, DRH1, DRL1, dU);
    UpDown(BoardList, Upwr, Ugnd, DRH, DRL, DRH1, DRL1, dU);

    //сбрасываем глобальные переменные
    First_Run := true;
    Last_Run := 1;

    //цикл по всем пинам
    for K :=  1 to NumOfPin do
      begin
        //пропускаем итерацию если вывод не в списке проверяемых
        if not(K in MeasPin) then continue;
        
	//проверка необходимости повторного запуска ФК
	if StopFK[Last_Run] <> StopFK[K] or First_Run then
          begin
       	    start_beg_hand(StartFK, StopFK[K], 1, 0, 1);
            repeat intStop := check_stop(intTact); DelayCompMks(100);
      	    until intStop <> 0;
      	    First_Run := false;
          end;
	
	//записываем номер последнего проверенного вывода
        Last_Run := K;

        //подключаем вывод к измерительной шине
        ConnectPinN(K, [Pin_To_DCM]);

	//при необходимости подключаем к ней же DCM
	if (mode and !0010) <> 0 then
	  begin
	    ConnectDCM(DCM_To_Pins);
	    DelayMS(TimeUSB);
	  end;
	
	//при необходимости увеличиваем ток DCM
	if IDCM > 1.0e-3 then
	  begin
	    SetDCM(UDCM, RAuto, IDCM, DCM_Auto);
	    DelayMS(TimeUSB);
	  end;
        DelayMs(TimeMeasI);

	//измеряем значение тока
	I := OnlyMeasDCMCurent;
        DelayMs(TimeUSB);
	
	//при необходимости уменьшаем ток DCM для разкоммутации
	if(IDCM > 1.0e-3) then
	  begin
            SetDCM(UDCM, RAuto, Iconnect, DCM_Auto);
            DelayMs(TimeUSB);
	  end;

        //при необходимости подключаем вывод к драйверам или отключаем в воздух
	if (K in ConnPins) then 
	  ConnectPinN(K, [Pin_To_Drivers]);
	else
	  ConnectPinN(K, []);
	  
	//если не выбран режим "не печати" выводим полученный результат
	if (mode and !10000) = 0 then
        //PrintResTU(TestName, PinNum,      Upwr, Value, LBound, UBound, Dim);
          PrintResTU(TestName,      K, Upwr-Ugnd,     I, LBound, UBound, Dim);  
      end;

    //отключаем DCM
    ConnectDCM(DCM_Off);
    DelayMS(TimeUSB);

    if (mode and !1000) <> 0 then
      begin
      
      //задаем нулевые уровни напряжения на источниках и драйверах
      //UpDown(   Boards, Upwr, Ugnd,  DRH,  DRL, DRH1, DRL1, dU);
	UpDown(BoardList, NULL, NULL, NULL, NULL, NULL, NULL, dU);
      
        ConnectPinsN(ConnPins, []);
      end;
    //возвращаем измеренное значение
    result := I;

  End;
//<Ili>

//<Ios>
//14
//Procedure IOS(Var MeasPin : TLargeSet; Upwr, Ugnd, UDCM, DRL, DRH, DRL1, DRH1, LBound, UBound, Dim : Real; StartFK : Integer; Var StopFK : TVectors; TestName : String);
//OutPins; Список проверяемых выводов
//5.0; Напряжение питания, В
//0.0; Смещение земли, В
//0.0; Выходное напряжение измерителя, В
//0.4; Напряжение низкого уровня, В
//4.5; Напряжение высокого уровня, В
//0.0; Доп.напряжение низкого уровня, В
//0.0; Доп.напряжение высокого уровня, В
//-30.0e-3; Нижняя граница, А
//-3.0e-3; Верхняя граница, А
//milli; Делитель (Uno: e-0, milli: e-3, micro: e-6, nano: e-9, pico: e-12)
//0000; Начальный вектор FK
//VectorIOS; Конечный вектор FK
//5.Ток.кор.замык.IOS,мА?5. Ток короткого замыкания IOS, мА; Имя теста
//Измерение тока короткого замыкания
//        IOS(MeasPin, Upwr, Ugnd, UDCM, DRL, DRH, DRL1, DRH1, LBound, UBound, Dim, StartFK, StopFK, TestName);
Procedure IOS(Var MeasPin : TLargeSet; Upwr, Ugnd, UDCM, DRL, DRH, DRL1, DRH1, LBound, UBound, Dim : Real; StartFK : Integer;
		    Var StopFK : TVectors; TestName : String);
  Var
    IDCM, I : Real;
  Begin
    //определяем максимальную границу для установки тока
    if ABS(LBound)> ABS(UBound) then
      IDCM := ABS(LBound)
    else
      IDCM := ABS(UBound);
    
    //устанавливаем ток на 50% больше границы или 1.79 мкА при малых токах
    if IDCM < 1.5e-6 then
      IDCM := 1.79e-6
    else
      IDCM := IDCM * 1.5;

    //убеждаемся в отсутствии коррекции при отключенном режиме смещенной земли
    if VEEON <> true then
      Ugnd := 0.0;
    
    //корректируем значения питаний с учетом смещенной земли 
    Upwr := Upwr + Ugnd;
    DRL  := DRL  + Ugnd;
    DRH  := DRH  + Ugnd;
    DRL1 := DRL1 + Ugnd;
    DRH1 := DRH1 + Ugnd;
    UDCM := UDCM + Ugnd;

  //устанавливаем нулевые уровни напряжений на источниках и драйверах 
  //UpDown(   Boards, Upwr, Ugnd,  DRH,  DRL, DRH1, DRL1, dU);
    UpDown(BoardList, NULL, NULL, NULL, NULL, NULL, NULL, dU);

    //при необходимости уменьшаем ток DCM на момент коммутации
    if IDCM > 1.0e-3 then
      SetDCM(UDCM, RAuto, Iconnect, DCM_1);
    else
      SetDCM(UDCM, RAuto, IDCM, DCM_Auto);
    DelayMs(TimeUSB);

    //отключаем DCM от измерительной шины
    ConnectDCM(DCM_Off);
    DelayMS(TimeUSB);
    
    //подключаем входные пины к драйверам
    ConnectPinsN(InPins, [Pin_To_Drivers]);

  //задаем значения напряжений на драйверах и источниках
  //UpDown(   Boards, Upwr, Ugnd, DRH, DRL, DRH1, DRL1, dU);
    UpDown(BoardList, Upwr, Ugnd, DRH, DRL, DRH1, DRL1, dU);

    //обнуляем глобальные переменные
    First_Run := true;
    Last_Run := 1;
    
    //цикл по всем выводам
    for K := 1 to NumOfPin do
      begin
        //если вывод не в списке измеряемых, пропускаем итерацию
        if not (K in MeasPin) then continue;
	//проверка необходимости повторного запуска ФК
	if (StopFK[Last_Run] <> StopFK[K]) or First_Run then
	  begin
	    start_beg_hand(StartFK, StopFK[K], 1, 0, 1);
	    repeat intStop := check_stop(intTact);
	    DelayCompMks(100);
	    until intStop <> 0;
	    First_Run := false;
	  end;
	
	//запоминаем номер последнего проверенного вывода
	Last_Run := K;

        //подключаем вывод к измерительной шине
	ConnectPinN(K, [Pin_To_DCM]);

        //подключаем DCM к измерительной шине
	ConnectDCM(DCM_To_Pins);
	DelayMs(TimeUSB);

        //при необходимости увеличиваем ток DCM
        if IDCM > 1.0e-3 then
	begin
	  SetDCM(UDCM, RAuto, IDCM, DCM_Auto);
	  DelayMs(trunc(TimeMeasI));
	end;
        
	//измеряем ток на выводе
	I := OnlyMeasDCMCurent;
	DelayMs(TimeUSB);

        //при необходимости уменьшаем ток DCM
        if IDCM > 1.0e-3 then
	  begin
	    SetDCM(UDCM, RAuto, Iconnect, DCM_1);
	    DelayMs(TimeUSB);
	  end;

	//отключаем вывод в воздух или подключаем его к драйверам
	if(K in InPins) then
	  ConnectPinN(K, [Pin_To_Drivers]);
	else
	  ConnectPinN(K, []);

        //отключаем от измерительной шины DCM
	ConnectDCM(DCM_Off);
	DelayMS(TimeUSB);

      //выводим измеренный результат
      //PrintResTU(TestName, PinNum,      Upwr, V, LBound, UBound, Dim);
	PrintResTU(TestName,      K, Upwr-Ugnd, I, LBound, UBound, Dim);
      end;

  End;
//<Ios>

//<Icc>
//12
//Procedure ICC(Upwr, Ugnd, DRL, DRH, DRL1, DRH1, LBound, UBound, Dim : Real; StartFK, StopFK : Integer; TestName : String);
//5.0; Напряжение питания, В
//0.0; Смещение земли, В
//0.4; Напряжение низкого уровня, В
//4.5; Напряжение высокого уровня, В
//0.0; Доп.напряжение низкого уровня, В
//0.0; Доп.напряжение высокого уровня, В
//-1.5e-6; Нижняя граница, А
//1.3e-3; Верхняя граница, А
//milli; Делитель (Uno: e-0, milli: e-3, micro: e-6, nano: e-9, pico: e-12)
//0000; Начальный вектор FK
//0000; Конечный вектор FK
//6.Ток.потребл.ICC,мА?6. Ток потребления ICC, мА; Имя теста
//Измерение тока потребления

//Переключение на DCM при 0В
Procedure ICC_ON;
  Begin
  //задаем нулевые напряжения на источниках и драйверах
  //UpDown(   Boards, Upwr, Ugnd,  DRH,  DRL, DRH1, DRL1, dU);
    UpDown(BoardList, NULL, NULL, NULL, NULL, NULL, NULL, dU);
    
    //задаем нулевое напряжение и минимальный ток на DCM
    SetDCM(NULL, R8, Iconnect, DCM_1);
    DelayMs(TimeUSB);

    //подключаем DCM вместо источника напряжения
    ConnectDCM(ComDCMPwr);
    DelayMs(TimeUSB);

    //устанавливаем ограничение DCM по току равное ограничению источников
    SetDCM(NULL, R8, IlimPwr, DCM_Auto);
    DelayMs(TimeUSB);

    //отключаем источник напряжения
    ConnectPower(PWR, Source_Off);
    DelayMs(TimeUSB);

    //сохраняем значение источника для последующего подключения
    PWROLD := PWR;
    PWR	   := pDCM;

    //отключаем выходные выводы
    ConnectPinsN(OutPins, []);

    //подключаем входные выводы к драйверам
    ConnectPinsN(InPins, [Pin_To_Drivers]);
  End;

//Измерение тока потребления
	//ICC(Upwr, Ugnd, DRL, DRH, DRL1, DRH1, LBound, UBound, Dim, StartFK, StopFK, TestName);
Procedure ICC(Upwr, Ugnd, DRL, DRH, DRL1, DRH1, LBound, UBound, Dim : Real; StartFK, StopFK : Integer; TestName : String);
  Var
    IDCM, I : Real;
  Begin
    //определяем максимальную границу для установки ограничения по току
    if ABS(LBound) > ABS(UBound) then
      IDCM := ABS(LBound);
    else
      IDCM := ABS(UBound);

    //устанавливаем ограничения по току на 50% больше границы или 1.79 мкА при малых токах
    if IDCM < 1.5e-6 then
      IDCM := 1.79e-6
    else
      IDCM := IDCM * 1.5;
    
    //убеждаемся, что при отключенном режиме смещенной земли коррекция равна 0
    if VEEON <> true then
      Ugnd := 0.0;

    //корректируем напряжения с учетом смещения земли
    Upwr := Upwr + Ugnd;
    DRL  := DRL  + Ugnd;
    DRH  := DRH  + Ugnd;
    DRL1 := DRL1 + Ugnd;
    DRH1 := DRH1 + Ugnd;
    
  //устанавливаем нужные уровни напряжения
  //UpDown(   Boards, Upwr, Ugnd, DRH, DRL, DRH1, DRL1, dU);
    UpDown(BoardList, Upwr, Ugnd, DRH, DRL, DRH1, DRL1, dU);

    SetDCM(Upwr, RAuto, ILimPwr, DCM_Auto);
    DelayMS(TimeUSB);
   
    //запускаем ФК
    start_beg_hand(StartFK, StopFK, 1, 0, 1);
    DelayMS(TimeMeasI*2);

    //уменьшаем ток DCM для снижения погрешности
    SetDCM(Upwr, RAuto, IDCM, DCM_Auto);
    DelayMS(TimeMeasI*2);

    //измеряем ток потребления
    I := (OnlyMeasDCMCurent + OnlyMeasDCMCurent + OnlyMeasDCMCurent) / 3;
    DelayMS(TimeUSB);
    
    //принудительная остановка ФК при измерении динамического тока
    StopPP;

    //увеличиваем ток DCM для последующих тестов
    SetDCM(Upwr, RAuto, ILimPwr, DCM_Auto);
    DelayMS(TimeUSB);

  //вывод измеренного результата
  //PrintResTU(TestName,   PinNum,      Upwr, V, LBound, UBound, Dim);
    PrintResTU(TestName, NumOfPin, Upwr-Ugnd, I, LBound, UBound, Dim);
  End;

//Переключение на источник при 0В
Procedure ICC_OFF;
  Begin
  //UpDown(   Boards, Upwr, Ugnd,  DRH,  DRL, DRH1, DRL1,   dU);
    UpDown(BoardList, NULL, NULL, NULL, NULL, NULL, NULL, 0.25);

    //возвращаем сохраненное ранее значение источника
    PWR := PWROLD;
    
    //включаем источник обратно))
    SetPower(PWR, NULL, ILimPwr, Source_On);
    DelayMS(TimeUSB);

    //задаем нулевое напряжение и минимальный ток на DCM
    SetDCM(NULL, R8, IConnect, DCM_1);
    DelayMS(TimeUSB);

    //отключаем DCM
    ConnectDCM(DCM_Off);
    DelayMS(TimeUSB);
  End;
//<Icc>

//<Fk>
//11
//Procedure FK(Upwr, Ugnd, DRL, DRH, DRL1, DRH1, CPL, CPH : Real; StartFK, StopFK : Integer; TestName: String);
//5.0; Напряжение питания, В
//0.0; Смещение земли, В
//0.4; Напряжение низкого уровня, В
//4.5; Напряжение высокого уровня, В
//0.0; Доп.напряжение низкого уровня, В
//0.0; Доп.напряжение высокого уровня, В
//0.8; Нижний уровень компарирования, В
//4.0; Верхний уровень компарирования, В
//0000; Начальный вектор FK
//0000; Конечный вектор FK
//7.Функцион.контр.FK,B?7. Функциональный контроль FK, В; Имя теста
//Проведение динамического ФК
//        FK(Upwr, Ugnd, DRL, DRH, DRL1, DRH1, CPL, CPH, StartFK, StopFK, TestName)
Procedure FK(Upwr, Ugnd, DRL, DRH, DRL1, DRH1, CPL, CPH : Real; StartFK, StopFK : Integer; TestName: String);
  Var
    FKState, StopVector	: Integer;
  Begin
  
    //обнуляем коррекцию при несмещенной земле
    if VEEON <> true then
      Ugnd := 0.0;
    
    //изменяем напряжения с учетом смещения земли
    Upwr := Upwr + Ugnd;
    DRL  := DRL  + Ugnd;
    DRH  := DRH  + Ugnd;
    CPL  := CPL  + Ugnd;
    CPH  := CPH  + Ugnd;
    DRL1 := DRL1 + Ugnd;
    DRH1 := DRH1 + Ugnd;

  //задаем уровни напряжений на драйверах и источниках
  //UpDown(   Boards, Upwr, Ugnd, DRH, DRL, DRH1, DRL1, dU);
    UpDown(BoardList, Upwr, Ugnd, DRH, DRL, DRH1, DRL1, dU);
    
    //задаем уровни компараторов
    LoadDACPinsLevels(BoardList, DRH, DRL, CPH, CPL, DRH1, DRL1);
    
    //подключаем все пины к драйверам
    ConnectPinsN(AllPins, [Pin_To_Drivers]);

    //запускаем ФК с оставкой при браке
    start_beg_hand(StartFK, StopFK, 1, 1, 1);
    repeat FKState := check_stop(StopVector); DelayCompMks(100);
    until  FKState <> 0;
    FKState := check_stop(StopVector);
    StopPP;
    
  //выводим результат выполнения ФК
  //PrintResTU(TestName, PinNum,       Upwr,          V, LBound, UBound, Dim);
    PrintResTU(TestName,     -1,  Upwr-Ugnd, StopVector, StopFK, StopFK, Uno); 

    //отключаем все выводы
    ConnectPinsN(AllPins, []);

  End;
//<Fk>

//<Tp>
//15
//Procedure Tp(Var MeasPin : TLargeSet; Upwr, Ugnd, DRL, DRH, DRL1, DRH1, CPL, CPH, TinT, UBound : Real; StartFK, StopFK: Integer; TestName: String; SFPMode : Boolean);
//OutPins; Список проверяемых выводов
//5.0; Напряжение питания, В
//0.0; Смещение земли, В
//0.4; Напряжение низкого уровня, В
//4.5; Напряжение высокого уровня, В
//0.0; Доп.напряжение низкого уровня, В
//0.0; Доп.напряжение высокого уровня, В
//2.20; Нижний уровень компарирования, В
//2.30; Верхний уровень компарирования, В
//Tin; Задержка распространения, переменная или число, нс
//15; Верхняя граница, нс
//0001; Начальный вектор FK
//0006; Конечный вектор FK
//8.Вр.зад.распр.TpHL,нс?8. Время задержки распространения TpHL, нс; Имя теста
//true; Выбор между режимом измерения с начала или конца вектора
//Измерение времени задержки
	//Tp(MeasPin,  Upwr, Ugnd, DRL, DRH, DRL1, DRH1, CPL, CPH,  TinT, UBound,  StartFK, StopFK,  TestName, SFPMode);
Procedure Tp(Var MeasPin : TLargeSet; Upwr, Ugnd, DRL, DRH, DRL1, DRH1, CPL, CPH, TinT, UBound : Real; StartFK,
		   StopFK: Integer; TestName: String; SFPMode : Boolean);
  Var
    Tp : Real;
    //переменная только для передачи в формовскую функцию
    //теоретически в нее записывается номер вектора с проверкой
    V : Integer;
  Begin
    //отключаем DCM
    ConnectDCM(DCM_Off);
    DelayMS(TimeUSB);
    
    //обнуляем коррекцию при несмещенной земле
    if VEEON <> true then
      Ugnd := 0.0;
    
    //корректируем напряжения с учетом смещения земли
    Upwr := Upwr + Ugnd;
    DRL  := DRL  + Ugnd;
    DRH  := DRH  + Ugnd;
    CPL  := CPL  + Ugnd;
    CPH  := CPH  + Ugnd;
    DRL1 := DRL1 + Ugnd;
    DRH1 := DRH1 + Ugnd;
    
  //устанавливаем напряжения на драйверах и источниках
  //UpDown(   Boards, Upwr, Ugnd, DRH, DRL, DRH1, DRL1, dU);
    UpDown(BoardList, Upwr, Ugnd, DRH, DRL, DRH1, DRL1, dU);
    
    //устанавливаем уровни компараторов
    LoadDACPinsLevels(BoardList, DRH, DRL, CPH, CPL, DRH1, DRL1);
    DelayMS(TimeUSB);
    
    //подключаем все пины к драйверам
    ConnectPinsN(AllPins, [Pin_To_Drivers]);
    
    //цикл по всем выводам
    for K := 1 to NumOfPin do
      begin
        //пропускаем итерацию если вывод не в списке проверяемых
        if not(K in MeasPin) then continue;

	//выбор метода проверки
	if SFPMode then
	  Tp := SFP(StartFK, StopFK, K + DeltaH, V);
	else
	  Tp := SRFP(StartFK, StopFK, K + DeltaH, V);

	Tp := Tp - TinT;
	  
	//при необходимости уменьшаем нижнюю границу с учетом задержки
	if (Tp < 0)  then
          begin
            if Tp + TinT > 0 then
            //PrintResTU(TestName, PinNum,      Upwr,  V, LBound, UBound, Dim);
	      PrintResTU(TestName,      K, Upwr-Ugnd, Tp,   -TinT, UBound, Uno);
  	    else
	    //PrintResTU(TestName, PinNum,      Upwr,  V, LBound, UBound, Dim);
	      PrintResTU(TestName,      K, Upwr-Ugnd, Tp,   NULL, UBound, Uno);
	  end
	else
        //PrintResTU(TestName, PinNum,      Upwr,  V, LBound, UBound, Dim);
	  PrintResTU(TestName,      K, Upwr-Ugnd, Tp,   NULL, UBound, Uno);
      end;

    //отключаем все выводы
    ConnectPinsN(AllPins, []);

  End;
//<Tp>

//<Tt>
//15
//Procedure   Tt(Var MeasPin : TLargeSet; Upwr, Ugnd, DRL, DRH, DRL1, DRH1, CP_10, CP_90, UBound: Real; StartFK, StopFK : Integer; TestName : String; SFPMode, SignalRise : Boolean);
//OutPins; Список проверяемых выводов
//5.0; Напряжение питания, В
//0.0; Смещение земли, В
//0.4; Напряжение низкого уровня, В
//4.5; Напряжение высокого уровня, В
//0.0; Доп.напряжение низкого уровня, В
//0.0; Доп.напряжение высокого уровня, В
//0.5; Нижний уровень компарирования (10%), В
//4.0; Верхний уровень компарирования (90%), В
//15; Верхняя граница, нс
//0001; Начальный вектор FK
//0006; Конечный вектор FK
//8.Вр.зад.распр.TtHL,нс?8. Время задержки распространения TtHL, нс; Имя теста
//true; Выбор между режимом измерения с начала или конца вектора
//true; Выбор между измерением фронта и спада (true - фронт)
//Измерение времени фронта/спада
         // Tt(    MeasPin, Upwr, Ugnd, DRL, DRH, DRL1, DRH1, CP_10, CP_90, UBound, StartFK, StopFK, TestName, Method, SFPMode, SignalRise);
Procedure   Tt(Var MeasPin : TLargeSet; Upwr, Ugnd, DRL, DRH, DRL1, DRH1, CP_10, CP_90, UBound: Real; StartFK, StopFK : Integer; TestName : String; SFPMode, SignalRise : Boolean);
  Var
    Tt    : Real;
    Tp_10 : Real;
    Tp_90 : Real;
    //переменная только для передачи в формовскую функцию
    //теоретически в нее записывается номер вектора с проверкой
    V  : Integer;

  Begin
    //отключаем DCM
    ConnectDCM(DCM_Off);
    DelayMS(TimeUSB);
    
    //обнуляем коррекцию при несмещенной земле
    if VEEON <> true then
      Ugnd := 0.0;
    
    //корректируем напряжения с учетом смещения земли
    Upwr   := Upwr  + Ugnd;
    DRL    := DRL   + Ugnd;
    DRH    := DRH   + Ugnd;
    CP_10  := CP_10 + Ugnd;
    CP_90  := CP_90 + Ugnd;
    DRL1   := DRL1  + Ugnd;
    DRH1   := DRH1  + Ugnd;
    
  //устанавливаем напряжения на драйверах и источниках
  //UpDown(   Boards, Upwr, Ugnd, DRH, DRL, DRH1, DRL1, dU);
    UpDown(BoardList, Upwr, Ugnd, DRH, DRL, DRH1, DRL1, dU);
    
    //устанавливаем уровни компараторов
    LoadDACPinsLevels(BoardList, DRH, DRL, CP_10, CP_10, DRH1, DRL1);
    DelayMS(TimeUSB);
    
    //подключаем все пины к драйверам
    ConnectPinsN(AllPins, [Pin_To_Drivers]);
    DelayMS(TimeUSB);

    //цикл по всем выводам
    for K := 1 to NumOfPin do
      begin
        //пропуск итерации если вывод не в списке проверяемых
        if not(K in MeasPin) then continue;
        
	//загружаем нужные значения компараторов
	LoadDACPinsLevels(BoardList, DRH, DRL, CP_10, CP_10, DRH1, DRL1);
	
	//выбор метода измерения
	if SFPMode then 
	  Tp_10 := SFP (StartFK, StopFK, K + DeltaH, V)
	else 
	  Tp_10 := SRFP(StartFK, StopFK, K + DeltaH, V);

        //загружаем вторые значения компараторов
        LoadDACPinsLevels(BoardList, DRH, DRL, CP_90, CP_90, DRH1, DRL1);
        DelayMS(TimeUSB);

        //выбор метода измерения
        if SFPMode then
          Tp_90 := SFP (StartFK, StopFK, K, V)
	else 
	  Tp_90 := SRFP(StartFK, StopFK, K, V);

        //вычисление итогового значения
	if SignalRise then 
	  Tt := Tp_90 - Tp_10
	else 
	  Tt := Tp_10 - Tp_90;

      //вывод полученного результата
      //PrintResTU(TestName, PinNum,      Upwr, Value, LBound, UBound, Dim);
        PrintResTU(TestName,      K, Upwr-Ugnd,    Tt,   NULL, UBound, Uno);
      end;

    //отключение всех выводов
    ConnectPinsN(AllPins, []);

  End;
//<Tt>

//<Ucdi>
//13
//Procedure UCDI_mod(Var MeasPin : TLargeSet; Upwr, Ugnd, DRL, DRH, DRL1, DRH1, IDCM, LBound, UBound : Real; StartFK : Integer; Var StopFK : TVectors; TestName : String);
//OutPins; Список проверяемых выводов
//5.0; Напряжение питания, В
//0.0; Смещение земли, В
//0.4; Напряжение низкого уровня, В
//4.5; Напряжение высокого уровня, В
//0.0; Доп.напряжение низкого уровня, В
//0.0; Доп.напряжение высокого уровня, В
//1.2e-3; Ток на проверяемом выводе, А
//-2.0; Нижняя граница, В
//-0.3; Верхняя граница, В
//0001; Начальный вектор FK
//VectorUCDI; Конечный вектор FK
//10.Пад.напр.на диоде UCDI,В?10. Падение напржения на антизвонном диоде UCDI, В; Имя теста
//Прямое падение напряжения на антизвонном диоде
        //UCDI(MeasPin, Upwr, Ugnd, DRL, DRH, DRL1, DRH1, IDCM, LBound, UBound, StartFK, StopFK, TestName);
Procedure UCDI(Var MeasPin : TLargeSet; Upwr, Ugnd, DRL, DRH, DRL1, DRH1, IDCM, LBound, UBound : Real; StartFK : Integer;
		   Var StopFK : TVectors; TestName : String);
  Var
    UDCM, UCDI : Real;
  Begin
    //определяем границу DCM по напряжению
    if ABS(LBound) > ABS(UBound) then
      UDCM := LBound*1.5
    else
      UDCM := UBound*1.5;

    //обнуляем коррекцию при несмещенной земле
    if VEEON <> true then
      Ugnd := 0.0;
    
    //корректируем напряжения с учетом смещения земли
    Upwr := Upwr + Ugnd;
    DRL  := DRL  + Ugnd;
    DRH  := DRH  + Ugnd;
    DRL1 := NULL + Ugnd;
    DRH1 := NULL + Ugnd;
    UDCM := UDCM + Ugnd;

  //задаем нулевые уровни напряжения на источниках и драйверах
  //UpDown(   Boards, Upwr, Ugnd,  DRH,  DRL, DRH1, DRL1, dU);
    UpDown(BoardList, NULL, NULL, NULL, NULL, NULL, NULL, dU);
    
    //подключаем входные пины к драйверам
    ConnectPinsN(InPins,[Pin_To_Drivers]);
    
    //устанавливаем уровень напряжения и тока на DCM
    SetDCM(UDCM, RAuto, Iconnect, DCM_Auto);
    DelayMs(TimeMeasU);
    
    //подключаем DCM к измерительной шине
    ConnectDCM(DCM_To_Pins);
    DelayMs(TimeUSB);

  //задаем уровни напряжений на драйверах и источниках
  //UpDown(   Boards, Upwr, Ugnd, DRH, DRL, DRH1, DRL1, dU);
    UpDown(BoardList, Upwr, Ugnd, DRH, DRL, DRH1, DRL1, dU);
    
    //обнуляем глобальные переменные
    First_Run:= TRUE;
    Last_Run := 0;

    //цикл по всем выводам
    for K := 1 to NumOfPin do
       begin
         //пропуск итерации если вывод не в списке проверяемых
         if not(K in MeasPin) then continue;
         
	 //проверка необходимости повторного запуска ФК
	 if (StopFK[Last_Run]<>StopFK[K]) or First_Run = true then
           begin
              start_beg_hand(StartFK, StopFK[K], 1, 0, 1);
              repeat  intStop := check_stop(intTact); DelayCompMks(100);
              until intStop <> 0;
              First_Run := false;
            end;
         //запоминаем последний проверенный вывод  
         Last_Run := K;
         
	 //подключаем вывод к измерителю
	 ConnectPinN(K, [Pin_To_DCM]);

	 //устанавливаем на нем нужные уровни тока и напряжения
         SetDCM(UDCM, RAuto, IDCM, DCM_Auto);
         DelayMs(TimeMeasU);

	 //измеряем напряжение
         UCDI := OnlyMeasDCMVoltage(ADCRange_AUTO);
         DelayMs(TimeUSB);

	 //уменьшаем ток для разкоммутации
         SetDCM(UDCM, RAuto, Iconnect, DCM_Auto);
         DelayMs(TimeUSB);

	 //подключаем вывод обратно к драйверам
         ConnectPinN(K, [Pin_To_Drivers]);

       //выводим измеренный результат
       //PrintResTU(TestName, PinNum,      Upwr, Value, LBound, UBound, Dim);
         PrintResTU(TestName,      K, Upwr-Ugnd,  UCDI, LBound, UBound, Uno);
       end;

     //отключаем DCM
     ConnectDCM(DCM_Off);
     DelayMS(TimeUSB);

     //отключаем все пины
     ConnectPinsN(AllPins, []);

  End;
//<Ucdi>
//<Endofsource>