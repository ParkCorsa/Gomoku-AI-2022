#include "AIController.h"
#include <utility>
#include <string>
#include <algorithm>
#include <set>
#include <vector>
#include <iostream>

#pragma GCC optimize(2)

using namespace std;

extern int ai_side; //0: black, 1: white
string ai_name = "Tensai";

const int DEP=12;
const int _DEP=6;

const int WID[DEP+1]={0, 0, 3, 3, 3, 3, 3, 4, 4, 5, 6, 7, 9};
const int _WID[_DEP+1]={0, 0, 3, 3, 4, 5, 7};

int turn = 0;

void init() {turn=0;}

vector<pair<int,int> >self,opp;

struct Node{//普通格子
    int x,y,w;
    Node(int _x=0,int _y=0):x(_x),y(_y){w=min(_x+1,15-_x)*min(_y+1,15-_y);}
    Node operator +(const Node& other)const{return Node(x+other.x,y+other.y);}
    Node operator -(const Node& other)const{return Node(x-other.x,y-other.y);}
    Node operator *(const int& t)const{return Node(x*t,y*t);}
    bool operator <(const Node& other)const{return w==other.w?(x==other.x?y<other.y:x<other.x):w<other.w;}
    bool operator ==(const Node& other)const{return x==other.x&&y==other.y;}
};

struct Blank{//空格子
    Node node;
    int w;
    Blank (Node _node,int _w):node(_node),w(_w){}
    bool operator <(const Blank& other)const{return w==other.w?other.node<node:other.w<w;}
};

struct cc{//联通分量，左边和右边连续相同颜色构成的连通块，用于计算节点得分
    int L,R;//左右两侧的联通范围
    bool tagL,tagR;//边界与空格子接壤还是与（棋盘边缘/对方棋子）接壤，用于判断死活
    cc():L(0),R(0),tagL(0),tagR(0){}
    int len()const{return L+R+1;}
    int _L()const{return L+tagL;}
    int _R()const{return R+tagR;}
    int calc()const{
        int LEN=len();
        if(LEN>=5)return 1<<20;
        else{
            if(!tagL&&!tagR)return 0;
            else if(tagL&&tagR)return 1<<(1<<LEN);
            else return 1<<(LEN<<1);
        }
    }
};

const Node d[4]={Node(0,1),Node(1,0),Node(1,1),Node(1,-1)};

class Board{

    vector<vector<int> >board;

    vector<vector<vector<vector<cc> > > >state;

    set<Blank>blank;

    int tag=-1;

    bool outtaBound(Node c){return c.x<0||c.y<0||c.x>=15||c.y>=15;}

    int& getType(const Node& c){
        if(outtaBound(c))return tag;//-1出界，2是指空格子，只有2类型的格子我们才纳入考虑范围（即被放到set中）
        return board[c.x][c.y];
    }

    vector<vector<cc> >& getState(const Node& c){return state[c.x][c.y];}

    int getWeight(const Node& node,int type){return getState(node)[0][type].calc()+getState(node)[1][type].calc()+getState(node)[2][type].calc()+getState(node)[3][type].calc();}

    void editState(const Node& node,int dir){
        if(getType(node)==-1)return;
        if(getType(node)==2)blank.erase(Blank(node,max(getWeight(node,0),getWeight(node,1))));
        Node _d=d[dir];
        for(int j=0;j<2;++j){
            cc &tmp=getState(node)[dir][j];
            for(tmp.L=0;getType(node-_d*(tmp.L+1))==j;++tmp.L);
            for(tmp.R=0;getType(node+_d*(tmp.R+1))==j;++tmp.R);
            tmp.tagL=(getType(node-_d*(tmp.L+1))==2);
            tmp.tagR=(getType(node+_d*(tmp.R+1))==2);
        }
        if(getType(node)==2)blank.insert(Blank(node,max(getWeight(node,0),getWeight(node,1))));
    }
    void editType(const Node& node,int type){
        if(getType(node)==-1)return;
        if(getType(node)==2)blank.erase(Blank(node,max(getWeight(node,0),getWeight(node,1))));
        if(type==2)blank.insert(Blank(node,max(getWeight(node,0),getWeight(node,1))));
        getType(node)=type;
        for(int i=0;i<4;++i){
            editState(node,i);
            Node _d=d[i];
            vector<cc>& tmp=getState(node)[i];
            for(int j=-max(tmp[0]._L(),tmp[1]._L());j<=tmp[0]._R()||j<=tmp[1]._R();++j)
                if(j)editState(node+_d*j,i);
        }
    }
    Blank dfs(int type,int dep,const int* wid,int low=-1e9,int high=1e9){
        if(dep==1||blank.size()==1)
            return Blank(blank.begin()->node,(dep<<1)*getWeight(blank.begin()->node,type));
        int lim=-1e9;
        Node idx;
        auto it=blank.begin();
        for(int i=0;i<wid[dep]&&i<(int)blank.size();++i,++it){
            Node tmp=it->node;
            int val=getWeight(tmp,type)*(dep<<1);
            if(val<1e6){
                editType(tmp,type);
                val-=dfs(type^1,dep-1,wid,val-high,val-low).w;
                editType(tmp,2);
                it=blank.find(Blank(tmp,max(getWeight(tmp,0),getWeight(tmp,1))));
            }
            if(val>lim)lim=val,idx=tmp;
            if(low>=high)break;
        }
        return Blank(idx,lim);
    }
public:
    Board():board(15,vector<int>(15,2)),state(15,vector<vector<vector<cc>>>(15,vector<vector<cc>>(4,vector<cc>(2)))){
        for(int i=0;i<15;++i)
            for(int j=0;j<15;++j)
                for(int k=0;k<4;++k)
                    editState(Node(i,j),k);
    }
    void update(int x,int y,int type){
        if(x==-1&&y==-1){
            for(int i=0;i<15;++i)
                for(int j=0;j<15;++j)
                    if(board[i][j]!=2)
                        update(i,j,board[i][j]^1);
        }
        else editType(Node(x,y),type);
    }
    Node normalTurn(){return dfs(0,DEP,WID).node;}
    Node bw(){//后手且准备下第二手
        int val=-1;
        Node ret;
        for(int i=0;i<15;++i)
            for(int j=0;j<15;++j)
                if(board[i][j]==2){
                    update(i,j,0);
                    int cur=abs(dfs(1,_DEP,_WID).w);
                    if(cur>val)val=cur,ret=Node(i,j);
                    update(i,j,2);
                }
        return ret;               
    }
    Node bwb(){//先手且之前已经下了不超过一手
        int val=1e9;
        Node ret;
        for(int i=0;i<15;++i)
            for(int j=0;j<15;++j)
                if(board[i][j]==2){
                    update(i,j,0);
                    int cur=abs(dfs(1,_DEP,_WID).w);
                    if(cur<val)val=cur,ret=Node(i,j);
                    update(i,j,2);
                }
        return ret;               
    }
    Node swap2(){//第三手
        Blank ret=dfs(0,DEP,WID);
        if(ret.w>0)return ret.node;
        else return Node(-1,-1);
    }
};

Board board;

pair<int, int> action(pair<int, int> loc) {
    board=Board();
    for(int i=0;i<turn;++i){
        board.update(opp[i].first,opp[i].second,1);
        board.update(self[i].first,self[i].second,0);
    }
    board.update(loc.first,loc.second,1),opp.push_back(loc);
    Node ret;
    if(turn<=1&&ai_side==0)ret=board.bwb();
    else if(!turn)ret=board.bw();
    else if(turn==1)ret=board.swap2();
    else ret=board.normalTurn();
    ++turn,self.emplace_back(make_pair(ret.x,ret.y));
    return make_pair(ret.x,ret.y);
}