// Part1.cpp : Этот файл содержит функцию "main". Здесь начинается и заканчивается выполнение программы.
//

//#include "stdafx.h"
#include <stdio.h>
#include <tchar.h>
#include <conio.h>
#include <math.h> 
#include <iostream>
#include <fstream>
#include <Windows.h>
#include <string>
#include <string.h>
#include <iomanip>
using namespace std;
// Создаем структуру, которая будет содержать информацию про WAVE формат
struct WAVEINFO {
	char chunkID[4]; // WAVE формат всегда начинается c RIFF заголовка 
	unsigned long chunkSize;
	char format[4]; // Будет содержать символы "WAVE" 
	char subchunk1Id; // Будет содержать символы "fmt " 
	unsigned long subchunk1Size;  // Цепь
	unsigned short audioFormat; //содержит формат сжатия 
	unsigned short numChannels; // кол-во каналов 
	unsigned long sampleRate; // частота дискретизации 
	unsigned long byteRate; // sampleRate*numChannels*bitsPerSample/8 кол-во байт переданных за секунду
	unsigned short blockAlign; //numChannels*bitsPerSampe/8 - кол-во байт для одного сэмпла, включая все каналы 
	unsigned short bitsPerSample; // Глубина или точность звучания (8, 16 бит и так далее) кол--во бит в сэмпле
	// Дальше идет цепочка содержит непосредственно ИНФОРМАЦИЮ про аудио-данные и их размер 
	char subchunk2Id_LIST[4]; // Символы "LIST" 
	unsigned long subchunk2Size_LIST; // Кол-во байт в области дополнительных данных, numSamples*numChannels*bitPerSample/8 
};
// AVal - массив анализируемых данных, Nvl - длина массива должна быть кратна степени 2.
// FTvl - массив полученных значений, Nft - длина массива должна быть равна Nvl.

const double TwoPi = 6.283185307179586;

void FFTAnalysis(double* AVal, double* FTvl, int Nvl, int Nft)
{
	int i, j, n, m, Mmax, Istp;
	double Tmpr, Tmpi, Wtmp, Theta;
	double Wpr, Wpi, Wr, Wi;
	double* Tmvl;

	n = Nvl * 2;
	Tmvl = new double[n];

	for (i = 0; i < n; i += 2)
	{
		//	cout << n << endl; 
		Tmvl[i] = 0;
		Tmvl[i + 1] = AVal[i / 2];
	}

	i = 1; j = 1;
	while (i < n) {
		if (j > i) {
			Tmpr = Tmvl[i]; Tmvl[i] = Tmvl[j]; Tmvl[j] = Tmpr;
			Tmpr = Tmvl[i + 1]; Tmvl[i + 1] = Tmvl[j + 1]; Tmvl[j + 1] = Tmpr;
		}
		i = i + 2; m = Nvl;
		while ((m >= 2) && (j > m)) {
			j = j - m; m = m >> 1;
		}
		j = j + m;
	}

	Mmax = 2;
	while (n > Mmax) {
		Theta = -TwoPi / Mmax;
		Wpi = sin(Theta);
		Wtmp = sin(Theta / 2);
		Wpr = Wtmp * Wtmp * 2;
		Istp = Mmax * 2;
		Wr = 1; Wi = 0; m = 1;

		while (m < Mmax) {
			i = m; m = m + 2;
			Tmpr = Wr;
			Tmpi = Wi;
			Wr = Wr - Tmpr * Wpr - Tmpi * Wpi;
			Wi = Wi + Tmpr * Wpi - Tmpi * Wpr;

			while (i < n) {
				j = i + Mmax;
				Tmpr = Wr * Tmvl[j] - Wi * Tmvl[j - 1];
				Tmpi = Wi * Tmvl[j] + Wr * Tmvl[j - 1];

				Tmvl[j] = Tmvl[i] - Tmpr; Tmvl[j - 1] = Tmvl[i - 1] - Tmpi;
				Tmvl[i] = Tmvl[i] + Tmpr; Tmvl[i - 1] = Tmvl[i - 1] + Tmpi;
				i = i + Istp;
			}
		}

		Mmax = Istp;
	}

	for (i = 0; i < Nft; i++) {
		j = i * 2; 
		FTvl[i] = 2 * sqrt(pow(Tmvl[j], 2) + pow(Tmvl[j + 1], 2)) / Nvl;
	}

	delete[]Tmvl;
}

// Функция вывода аудиоданных в файл
void file_out_samples(char* file_name, long count_samples_function, short int* Data)
{
	double x = 0;
	// Вывод массива сэмлов в текстовой файл 
	ofstream file_out(file_name, ios::trunc);
	for (int i = 0; i < count_samples_function; i++)
	{
		//	x = (double)(INT16)Data[i] / 0x8000;
		file_out << x << endl;
	}
}
void file_out_hanning(char* file_name, long count_samples_function, double* after_hanning)
{
	ofstream file_out(file_name, ios::trunc);
	for (int i = 0; i < count_samples_function; i++)
	{
		file_out << after_hanning[i] << endl;
	}
}

double Hanning(short int* Data1, double* after_hanning, long count_samples_function, int count_samples_per_100ms_int, int count_samples_per_50ms_int)
{
	int begin_window = 0;
	int end_window = count_samples_per_100ms_int;
	long double x = 0;
	int i = 0;
	int j = 1;
	while (end_window < count_samples_function)
	{
		for (i = begin_window; i < end_window; i++)
		{
			after_hanning[i] = (0.53836 - 0.46164 * cos(3.14 / 180 * (2 * 3.14 * j) / ((long double)end_window - begin_window - 1)));
			//	x = (double)(INT16)Data1[i] / 0x8000;
			x = Data1[i];
			after_hanning[i] = after_hanning[i] * x;
			j++;
		}
		begin_window = end_window - count_samples_per_50ms_int;
		end_window = end_window + count_samples_per_50ms_int;
		j = 1;
	}
	return 0;
}
double to_mel(double* fourier_data, long count_samples_function)
{
	for (int i = 0; i < count_samples_function; i += 1)
		fourier_data[i] = 1000 * log(1 + fourier_data[i] / 1000) / log(2);
	return 0;
}

int main()
{
	setlocale(LC_ALL, "Russian");
	// Краткий брифинг программы 
	cout << endl;
	cout << "**************Программа извлекает аудиоданные из .WAV файла******************" << endl << endl;
	cout << "Принимаем за оконную функцию функцию Хэмминга" << endl;
	cout << "За длину кадра будем брать значение равное 100 мс" << endl << endl;
	cout << "*****************************************************************************" << endl;

	FILE* file_in;
	errno_t err;
	err = fopen_s(&file_in, "1.wav", "rb");
	if (err)
	{
		cout << "Не удалось открыть файл: " << err << endl;
		system("pause");
		return 0;
	}
	// Переходим в конец аудиофайла, для вычисления его размера
	fseek(file_in, 0, SEEK_END);
	long nFileLen = ftell(file_in);
	// Возвращаемся в начало аудиофайла
	fseek(file_in, 0, SEEK_SET);
	// Считываем структуру WAVEINFO, в котором содержится нужная для дальнейших вычислений информация
	WAVEINFO header;
	fread_s(&header, sizeof(WAVEINFO), sizeof(WAVEINFO), 1, file_in);

	/*
	// Формируем динамический массив ДОПОЛНИТЕЛЬНЫХ ДАННЫХ размера БАЙТОВ ПОД ДОПОЛНИТЕЛЬНЫЕ ДАННЫЕ
		char *list_information = new char[header.subchunk2Size_LIST];
		Считываем эти данные из файла
		fread_s(list_information, sizeof(list_information), sizeof(list_information), 1, file_in);
		long lSize = ftell(file_in); // Позиция в считывании файла
		cout << lSize << endl;
	*/


	//Переходим к непосредственно аудиоданным, смещая указатель на N байтов (через доп. информацию в аудиофайле)
	fseek(file_in, header.subchunk2Size_LIST, SEEK_CUR);
	// Формируем массив под символы "DATA"
	char subchunk2Id[4];
	fread_s(&subchunk2Id, sizeof(subchunk2Id), sizeof(subchunk2Id), 1, file_in);

	// Для проверки корректного считывания доп. информации нужно расскоментировать следующие строки. 
	// Должна выводиться строка 'data' 
		/*
	for (int i = 0; i < 4; i++)
		cout << subchunk2Id[i];
		*/

		// Обьявляем переменную и записываем в нее КОЛ-ВО БАЙТОВ, на число которых нужно СМЕСТИТЬСЯ ПО ФАЙЛУ ВПЕРЕД 
		// К самим аудиоданным 

	unsigned long subchunk2Size;
	fread_s(&subchunk2Size, sizeof(subchunk2Size), sizeof(subchunk2Size), 1, file_in);


	long lSize = ftell(file_in); // Позиция в считывании файла
	long count_samples = (nFileLen - lSize) / (header.bitsPerSample / 8);
	cout << "Размер файла: " << nFileLen / 1024 << " KB" << endl;
	cout << "Кол-во байтов, отводимое на данные аудиофайла: " << lSize << endl;
	cout << "Кол-во байт в области данных: " << (subchunk2Size) << endl;
	cout << "Кол-во байтов, переданных в секунду: " << header.byteRate << endl;
	cout << "Кол-во каналов аудиозаписи: " << header.numChannels << endl;
	cout << "Квантование: " << header.audioFormat << endl;
	cout << "Частота дискретизации: " << header.sampleRate << "Гц" << endl;
	cout << "Кол-во байт для одного сэмпла, включая все каналы: " << header.blockAlign << endl;
	cout << "Точность звучания (глубина): " << header.bitsPerSample << "bit" << endl;
	cout << "Кол-во сэмплов (вычисленных вручную): " << subchunk2Size * 8 / header.bitsPerSample << endl;
	cout << "Кол-во сэмплов (из блока данных): " << count_samples << endl;
	cout << "Кол-во сэмплов на один канал: " << count_samples / 2 << endl;

	// Вычисление продолжительности аудиофайла

	long float fDurationSeconds = 1.f * (nFileLen - lSize) / (header.bitsPerSample / 8) / header.numChannels / header.sampleRate;
	int iDurationMinutes = ((int)floor(fDurationSeconds) / 60);
	long float fDurationSecondsForOut = fDurationSeconds - (iDurationMinutes * 60);
	printf_s("Продолжительность: %02d:%02.f\n", iDurationMinutes, fDurationSecondsForOut);
	cout << "В секундах: " << fDurationSeconds << endl;

	long int middle_sample = count_samples / 2;

	// Инициализация динамического массива для хранения сэмплов
	// Будут рассматриваться те аудиофайлы, у которых кол-во байтов на один сэмпл будет 2  
	// Поэтому и тип short int - 2 байта
	short int* Data = new short int[count_samples / 2];
	memset(Data, 0, sizeof(short int) * count_samples / 2);

	int count_bytes_per_sample_1_channel = header.blockAlign / header.numChannels;

	// Делим на два, потому что у диктофонной записи один канал записи. Однако при форматировании образуется второй канал связи
	// И второй канал заполняется точно такими же значениями, что и в первом 
	for (int i = 0; i < count_samples / 2; i++)
	{
		fread(&Data[i], count_bytes_per_sample_1_channel, 1, file_in);
		fseek(file_in, count_bytes_per_sample_1_channel, SEEK_CUR);
	}
	double DurationSeconds_per_sample = fDurationSeconds * header.numChannels / (count_samples);
	std::cout << "Секунд на каждый сэмпл: " << std::fixed << DurationSeconds_per_sample << endl;
	// Вычисление кол-ва сэмплов в каждом окне Хэмминга
	// В качестве ширины окна будем брать 100мс с перекрытием в 50мс 

	float ms100 = 0.1;
	float ms50 = 0.05;

	int count_samples_per_100ms_int = header.sampleRate / 10;
	int count_samples_per_50ms_int = header.sampleRate / 20;
	std::cout << "Кол-во сэмплов в каждом окне функции: " << std::fixed << count_samples_per_100ms_int << endl;
	std::cout << "Кол-во сэмплов в перекрытие окна функции: " << std::fixed << count_samples_per_50ms_int << endl;

	fclose(file_in);


	// Подготовительный участок кода для формирования цикла записей в файлы
	// Используется функция file_out_samples 
	// В качестве аргументов передается ИЗМЕНЯЕМОЕ название файла для вывода, кол-во сэмплов и сам массив данных 
	int num;
	char file_name_for_out[20] = "0";
	num = atoi(file_name_for_out);
	num++;
	_itoa_s(num, file_name_for_out, 10);				//------------
	strcat_s(file_name_for_out, "-example.txt");		//------------
	file_out_samples(file_name_for_out, count_samples / 2, Data);

	// Создание динамического массива для оконногой функции Хэмминга 
	double* after_hanning = new double[count_samples / header.numChannels];
	memset(after_hanning, 0, sizeof(double) * count_samples / header.numChannels);
	Hanning(Data, after_hanning, count_samples / header.numChannels, count_samples_per_100ms_int, count_samples_per_50ms_int);

	//Здесь я делал изменение  ---------------
	file_out_hanning((char*)"Окно.txt", count_samples / header.numChannels, after_hanning);

	double* f_fourier_data = new double[count_samples / header.numChannels];
	memset(f_fourier_data, 0, sizeof(double) * count_samples / header.numChannels);


	// Вычисление модуля спектра действительного массива чисел на основе реализации быстрого преобразования Фурье 
	// на преобразование должны передаваться кол-во элементов в степени 2, т.е. 4096 - 2^12
	int steps_fourier = 0;
	for (int i = 4096; steps_fourier + 4096 < count_samples / header.numChannels; steps_fourier += 4096)
	{
		FFTAnalysis(after_hanning + steps_fourier, f_fourier_data + steps_fourier, i, i);
		cout << steps_fourier << endl;
		//	steps_fourier += 4096; 
	}
	//FFTAnalysis(after_hanning, f_fourier_data, 4096, 4096);
	file_out_hanning((char*)"Fourier.txt", count_samples / header.numChannels, f_fourier_data);
	to_mel(f_fourier_data, count_samples / header.numChannels);

	num = atoi(file_name_for_out);
	system("pause");
	return 0;
}


