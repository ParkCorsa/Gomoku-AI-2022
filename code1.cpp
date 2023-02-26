#include "AIController.h"
#include <utility>
#include <cstring>
#include <climits>

extern int ai_side; //0: black, 1: white
std::string ai_name = "your_ai_name_here";

int turn = 0;
int board[15][15];
int dx[4]={0,1,1,1};
int dy[4]={1,0,1,-1};

//init function is called once at the beginning
void init() {
	/* TODO: Replace this by your code */
	memset(board, -1, sizeof(board));
}

// 连五，100000
// 活四, 10000
// 活三 1000
// 活二 100
// 活一 10
// 死四, 1000
// 死三 100
// 死二 10

bool out_of_bound(int x,int y){return x<0||y<0||x>=15||y>=15;}

bool check(int x,int y){return x>=0&&y>=0&&x<15&&y<15&&board[x][y]==-1;}

int calcBoard(){
    int ret=0;
    //没到边界的
    for(int i=0;i<15;++i)
        for(int j=0;j<15;++j){
            for(int k=0;k<4;++k)
                for(int l=1;l<5;++l){
                    if(out_of_bound(i+l*dx[k],j+l*dy[k])||board[i+(l-1)*dx[k]][j+(l-1)*dy[k]]!=board[i+l*dx[k]][j+l*dy[k]]){
                        if(l==4){
                            if(!out_of_bound(i-dx[k],j-dy[k])&&board[i+l*dx[k]][j+l*dy[k]]==-1)ret+=10000;
                            if(!out_of_bound(i-dx[k],j-dy[k])&&board[i-dx[k]][j-dy[k]]==board[i][j])ret+=10000;
                        }  
                        if(l==3)
                            if(!out_of_bound(i-dx[k],j-dy[k])&&board[i-dx[k]][j-dy[k]]==board[i][j])ret+=1000;
                        if(l==2)
                            if(!out_of_bound(i-dx[k],j-dy[k])&&board[i-dx[k]][j-dy[k]]==board[i][j])ret+=100;
                        if(l==1)
                            if(!out_of_bound(i-dx[k],j-dy[k])&&board[i-dx[k]][j-dy[k]]==board[i][j])ret+=10;
                        break;
                    }
                    if(l==4)ret+=100000;
                }            
        }

    return ret;
}

int maxval(int x,int y,int alpha,int beta,int side){
    int val=INT_MIN;
    for(int i=0;i<4;++i){
        int nx=x+dx[i],ny=y+dy[i];
        if(!check(nx,ny))continue;
        board[nx][ny]=side;
        val=std::max(val,std::max(calcBoard(),minval(nx,ny,alpha,beta,1-side)));
        board[nx][ny]=-1;
        if(val>=beta)return val;
        alpha=std::max(alpha,val);
    }
    for(int i=0;i<4;++i){
        int nx=x-dx[i],ny=y-dy[i];
        if(!check(nx,ny))continue;
        board[nx][ny]=side;
        val=std::max(val,std::max(calcBoard(),minval(nx,ny,alpha,beta,1-side)));
        board[nx][ny]=-1;
        if(val>=beta)return val;
        alpha=std::max(alpha,val);
    }
    return val;
}

int minval(int x,int y,int alpha,int beta,int side){
    int val=INT_MAX;
    for(int i=0;i<4;++i){
        int nx=x+dx[i],ny=y+dy[i];
        if(!check(nx,ny))continue;
        board[nx][ny]=side;
        val=std::min(val,std::min(calcBoard(),maxval(nx,ny,alpha,beta,1-side)));
        board[nx][ny]=-1;
        if(val<=alpha)return val;
        beta=std::min(beta,val);
    }
    for(int i=0;i<4;++i){
        int nx=x-dx[i],ny=y-dy[i];
        if(!check(nx,ny))continue;
        board[nx][ny]=side;
        val=std::min(val,std::min(calcBoard(),maxval(nx,ny,alpha,beta,1-side)));
        board[nx][ny]=-1;
        if(val<=alpha)return val;
        beta=std::min(beta,val);
    }
    return val;
}

std::pair<std::pair<int,int>,int> getnxt(){

}


// loc is the action of your opponent
// Initially, loc being (-1,-1) means it's your first move
// If this is the third step(with 2 black ), where you can use the swap rule, your output could be either (-1, -1) to indicate that you choose a swap, or a coordinate (x,y) as normal.

std::pair<int, int> getRandom() {
    while (true) {
        int x = rand() % 15;
        int y = rand() % 15;
        if (board[x][y] == -1) {
            board[x][y] = ai_side;
            return std::make_pair(x, y);
        }
    }
}

std::pair<int, int> action(std::pair<int, int> loc) {
    ++turn;
    if(loc.first==-1&&loc.second==-1){
        return getRandom();
    }
    board[loc.first][loc.second] = 1 - ai_side;
    
}