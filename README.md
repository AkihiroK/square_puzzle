# square_puzzle

* 作成者: Akihiro.K
* 作成理由: 授業課題
* 参考文献: https://yamakatsusan.web.fc2.com/python12.html

---

### 各パラメータについて
* ```mul_heuristic```  
heuristic関数で推定したコストに掛け算する値.(default = 1)

* ```heuristic_type```  
heuristic関数の計算方法を決める値.(0:定数(0), 1:正解配置と異なるピースの個数, 2:マンハッタン距離)

* ```board_size```  
ボードのサイズ（一辺）, 今回は 3 or 4　のみ対応  

