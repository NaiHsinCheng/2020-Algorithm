/*
   Author：B062040027 鄭乃心 B06401100 徐筱媛
   Date：2020.09.30
   Purpose：暴力法找最短路徑
*/

#include <iostream>
#include <fstream>
#include <stdlib.h> 
#include <math.h>
#include <time.h>
using namespace std;

void Permutations(int *a,int *ci, const int k, const int m, int* x, int* y,float *min, int *r){		//排列a[k]~a[m]
	if(k==m){
		float sum=0;
		for(int I=0; I<=m; I++){
			cout<<ci[a[I]-1]<<' ';
			if(I==m){
				sum+=sqrt(pow((x[a[I]-1]-x[a[I-1]-1]),2)+pow((y[a[I]-1]-y[a[I-1]-1]),2));	//計算兩點間距離
				sum+=sqrt(pow((x[a[I]-1]-x[a[0]-1]),2)+pow((y[a[I]-1]-y[a[0]-1]),2));	//計算第一點與最後一點的距離
			}else if(I>0){
				sum+=sqrt(pow((x[a[I]-1]-x[a[I-1]-1]),2)+pow((y[a[I]-1]-y[a[I-1]-1]),2));	//計算兩點間距離
			}
		}
		if(sum < *min || *min == 0){				//找出best distance
			*min = sum;				
			for(int I=0; I<=m; I++){			//紀錄best distance的排列
				r[I]=ci[a[I]-1];
			}	
		}
		cout << " --> Distance: " << sum << endl;
	}else{
		for(int I=k; I<=m; I++){
			swap(a[k],a[I]);
			Permutations(a,ci,k+1,m,x,y,&*min,r);
			swap(a[k],a[I]);
		}
	}
}

int main(){
	string name;
	cin>>name;
	int start=clock();
	
	fstream file;
	char buffer[80];		//存取讀檔案時的一列
	int count=0;			//城市數量
	file.open(name,ios::in);		//讀檔案，先算總共有個城市
	if(!file)
		cout << "檔案無法開啟\n" << endl;
	else{
		while(file.getline(buffer,sizeof(buffer),'\n')){
			count++;
		}
		file.close();
	}
	int X[count],Y[count];				//記錄每個城市的位置
	int City[count];
	char *p;				//儲存分割結果
	const char *split=" ";		//分割依據
	count=0;			//count歸零
	file.open(name,ios::in);		//再讀一次檔案，記錄每個位置
	if(!file)
		cout << "檔案無法開啟\n" << endl;
	else{
		while(file.getline(buffer,sizeof(buffer))){
			p = strtok(buffer,split); 	//分割字元陣列
			City[count]=atoi(p);
			p = strtok(NULL,split);
			X[count]=atoi(p);			//記錄位置 atoi() char轉int
			p = strtok(NULL,split);
			Y[count]=atoi(p);
			count++;
		}
		file.close();
	}

	//以上為讀檔與記錄城市位置，以下開始計算距離

	float min=0;					//最短路徑長
	int result[count];				//紀錄最短路徑長的排列
	int number[count];
	for(int I=1; I<=count;I++){
		number[I-1]=I;
	}
	Permutations(number,City,1,count-1,X,Y,&min,result);	//排列全部的點
	cout<<"Best Vist Order: ";
	for(int I=0;I<count;I++){
		cout<< result[I] <<' ';
	}
	cout<<endl;
	cout<<"Best Distance: "<< min <<endl;
	cout<<"Execution Time: "<< (double)(clock() - start) / CLOCKS_PER_SEC <<"(s)"<<endl;

	//寫出給gnuplot畫圖的檔案
	fstream f;
	f.open("data.txt",ios::out);
	if(f.fail())
		cout<<"檔案無法開啟"<<endl;
	else{
		for(int I=0;I<count;I++){
			f << X[result[I]-1]<<' '<< Y[result[I]-1]<<endl;
		}
		f << X[0]<<' '<< Y[0]<<endl;
		f.close();
	}
	
}

