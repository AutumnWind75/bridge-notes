// src/data/questions.js

export const questions = [
  {
    id: 1,
    dealer: "N", // 北家发牌
    vul: "双无",
    myHand: "S:J.H:AQJ9.D:AJ74.C:QJ63", 
    script: {
      start: { 
        turn: "player", 
        preBids: { N: "Pass", E: "Pass" },
        next: { 
          "1D": "ai_w_double", 
          "Pass": "end_fail_pass", 
          "1H": "end_fail_h", 
          "1S": "end_fail_s", 
          "1C": "end_fail_c", 
          "1NT": "end_fail_nt" 
        } 
      },
      ai_w_double: { 
        turn: "ai", 
        bids: { W: "X" }, 
        next: "ai_n_3h" 
      },
      ai_n_3h: {
        turn: "ai",
        bids: { N: "3H", E: "Pass" },
        next: "player_second"
      },
      player_second: {
        turn: "player",
        next: {
          "4H": "end_success_4h",
          "Pass": "end_success_pass"
        }
      },
      end_success_4h: { turn: "end", message: "非常好！由于 N 叫出了 3♥ 阻击，虽然你有 16 点，但持有 ♥AQJ9 的 4 张强支持，直接补足到 4♥ 进局是非常合理的选择。" },
      end_success_pass: { turn: "end", message: "非常聪明！N 的 3♥ 是阻击叫（表示点力不多但红心很长，局况有利）。你手里虽然有 16 点，但 ♠J 是废点，这牌往往很难拿到 10 墩，Pass 止叫 3♥ 是稳妥的决定。" },
      end_fail_pass: { turn: "end", message: "这次不对。这手牌有 16 点，且有 ♦AJ74，N 和 E 都 Pass 了，应该开叫 1♦，不能 Pass。" },
      end_fail_h: { turn: "end", message: "错误。虽然你有 ♥AQJ9，但只有 4 张，且不符合先叫长套的原则。你应该先叫 1♦。" },
      end_fail_s: { turn: "end", message: "错误。♠ 只有单张 J，无法开叫 1♠。" },
      end_fail_c: { turn: "end", message: "错误。♦ 套比 ♣ 套更好，且开叫 1♦ 能更好地描述你的 4-4-4-1 牌型。" },
      end_fail_nt: { turn: "end", message: "这次不对。虽然你有 16 点，但 ♠ 只有单张，无将定约非常危险；应优先开叫 1♦。" }
    }
  },
  // 以后在这里继续加第 2 题、第 3 题...
];