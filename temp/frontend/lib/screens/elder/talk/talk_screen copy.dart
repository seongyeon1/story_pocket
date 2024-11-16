import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:math';
import 'package:speech_to_text/speech_to_text.dart' as stt;
import 'package:flutter_tts/flutter_tts.dart';
import 'dart:async';

class TalkScreen extends StatefulWidget {
  const TalkScreen({super.key});

  @override
  State<TalkScreen> createState() => _TalkScreenState();
}

class _TalkScreenState extends State<TalkScreen> {
  final TextStyle speechBalloonText =
      const TextStyle(fontSize: 17, fontWeight: FontWeight.w600);
  final FlutterTts _tts = FlutterTts();
  late stt.SpeechToText _speech;
  bool _isListening = false;
  bool _isSpeaking = false;
  bool _showSuggestions = true;
  String _recognizedText = '';
  String _responseText = '안녕하세요! 오늘은 어떤 이야기를 할까요?';
  String _sessionId = 'session_id1';
  String sex = '할아버지';
  Timer? _stopListeningTimer;
  final int _noInputTimeout = 5;

  @override
  void initState() {
    super.initState();
    _speech = stt.SpeechToText();
    _initializeTTS();
    _generateSessionId();
  }

  void _initializeTTS() async {
    await _tts.setLanguage("ko-KR");
    await _tts.setVolume(0.9);
    _tts.setCompletionHandler(() => setState(() => _isSpeaking = false));
  }

  void _generateSessionId() {
    final random = Random();
    _sessionId =
        List.generate(10, (index) => random.nextInt(10).toString()).join();
  }

  Future<void> _listenAndRespond() async {
    if (_isSpeaking) {
      await _tts.stop();
      setState(() => _isSpeaking = false);
      return;
    }

    if (!_isListening) {
      setState(() => _showSuggestions = false);
      bool available = await _speech.initialize();
      if (available) {
        setState(() => _isListening = true);
        _speech.listen(
          onResult: (result) {
            setState(() {
              _recognizedText = result.recognizedWords;
            });
          },
          localeId: "ko_KR",
        );
        _resetStopListeningTimer();
      }
    } else {
      _stopListening();
    }
  }

  Future<void> _generateStory() async {
    final url = Uri.parse('http://127.0.0.1:8000/story/$_sessionId');
    try {
      final response = await http.get(url);
      if (response.statusCode == 200) {
        final responseBody = json.decode(utf8.decode(response.bodyBytes));
        showDialog(
          context: context,
          builder: (BuildContext context) {
            return AlertDialog(
              title: const Text("이야기 생성 완료"),
              content: Text(responseBody['story']),
              actions: [
                ElevatedButton(
                  onPressed: () => Navigator.pop(context),
                  child: const Text("닫기"),
                ),
              ],
            );
          },
        );
      } else {
        _showError("Error: ${response.statusCode}");
      }
    } catch (e) {
      _showError("이야기 생성에 실패했습니다.");
    }
  }

  void _showError(String message) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: const Text("오류"),
          content: Text(message),
          actions: [
            ElevatedButton(
              onPressed: () => Navigator.pop(context),
              child: const Text("닫기"),
            ),
          ],
        );
      },
    );
  }

  // 추천 질문 리스트 생성
  List<String> _getRandomSuggestions() {
    List<String> suggestions = [
      '오늘 식사는 어떠셨어요?',
      '요즘 가장 행복한 순간은 언제였나요?',
      '어제는 뭐하셨나요?',
      '오늘 기분은 어떠세요?',
      '추억의 음식이 있나요?',
      '어렸을 때 자주 놀던 놀이는 무엇인가요?',
      '어릴 적 가족과의 추억은?',
      '가장 좋아하는 노래는 뭐였나요?',
      '옛날에 자주 가셨던 곳은?',
    ];
    suggestions.shuffle();
    return suggestions.take(2).toList();
  }

  Widget _buildSuggestedQuestions() {
    List<String> _suggestions = _getRandomSuggestions();

    return Container(
      height: 50, // 고정된 높이
      child: ListView.builder(
        scrollDirection: Axis.horizontal,
        itemCount: _suggestions.length,
        itemBuilder: (context, index) {
          return Padding(
            padding: const EdgeInsets.symmetric(horizontal: 5.0),
            child: ElevatedButton(
              onPressed: () {
                setState(() {
                  _responseText = _suggestions[index];
                  _showSuggestions = false; // 추천 질문 숨기기
                });
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.lightGreen,
              ),
              child: Text(
                _suggestions[index],
                style: const TextStyle(fontSize: 16, color: Colors.white),
              ),
            ),
          );
        },
      ),
    );
  }

  Widget _buildSpeechBalloon(String text) {
    final textPainter = TextPainter(
      text: TextSpan(text: text, style: speechBalloonText),
      textDirection: TextDirection.ltr,
    );
    textPainter.layout(maxWidth: 250);

    final textWidth = textPainter.size.width;
    final textHeight = textPainter.size.height;

    // 고정 크기로 말풍선 크기를 제한
    final balloonWidth = textWidth + 60;
    final balloonHeight = textHeight + 40;

    return Stack(
      alignment: Alignment.center,
      children: [
        Container(
          width: balloonWidth,
          height: balloonHeight,
          decoration: BoxDecoration(
            image: DecorationImage(
              image: AssetImage('assets/image/square-speech-bubble.png'),
              fit: BoxFit.fill,
            ),
          ),
        ),
        Padding(
          padding: const EdgeInsets.all(20.0),
          child: SizedBox(
            width: 250,
            child: Text(
              text,
              textAlign: TextAlign.center,
              style: speechBalloonText,
            ),
          ),
        ),
      ],
    );
  }

  void _resetStopListeningTimer() {
    _stopListeningTimer?.cancel();
    _stopListeningTimer = Timer(Duration(seconds: _noInputTimeout), () {
      _stopListening();
    });
  }

  void _stopListening() async {
    if (_isListening) {
      _speech.stop();
      setState(() => _isListening = false);
      if (_recognizedText.isNotEmpty) {
        _sendMessage(_recognizedText);
      }
    }
  }

  Future<void> _sendMessage(String message) async {
    final url = Uri.parse('http://127.0.0.1:8000/chat/');
    final headers = {
      "accept": "application/json",
      "Content-Type": "application/json",
    };
    final body = json.encode({
      "sex": sex,
      "message": message,
      "session_id": _sessionId,
    });

    try {
      final response = await http.post(url, headers: headers, body: body);
      if (response.statusCode == 200) {
        final responseBody = json.decode(utf8.decode(response.bodyBytes));
        setState(() {
          _responseText = responseBody['response'];
          _tts.speak(_responseText);
          _isSpeaking = true;
        });
      } else {
        setState(() {
          _responseText = "Error: ${response.statusCode}";
        });
      }
    } catch (e) {
      setState(() {
        _responseText = "서버 연결에 실패했습니다.";
      });
    }
  }

  @override
  void dispose() {
    _stopListeningTimer?.cancel();
    _speech.stop();
    _tts.stop();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        actions: [
          IconButton(
            onPressed: () {},
            icon: const Icon(Icons.notifications),
          ),
          IconButton(
            onPressed: () {},
            icon: const Icon(Icons.account_circle_rounded),
          )
        ],
      ),
      body: LayoutBuilder(
        builder: (context, constraints) {
          return Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Text("마이크 버튼을 클릭하고 대화를 시작해 보세요!"),
              const SizedBox(height: 20),

              // AI 응답 말풍선
              _buildSpeechBalloon(_responseText),

              Image.asset(
                'assets/image/girl.png',
                height: 300,
              ),

              if (_recognizedText.isNotEmpty)
                Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: Text(
                    "사용자: $_recognizedText",
                    textAlign: TextAlign.center,
                    style: speechBalloonText,
                  ),
                ),

              IconButton(
                onPressed: _listenAndRespond,
                icon: Icon(
                  _isListening ? Icons.mic : Icons.mic_none,
                  size: 45,
                  color: _isListening ? Colors.red : Colors.blueAccent,
                ),
              ),
              const SizedBox(height: 20),

              if (_showSuggestions) _buildSuggestedQuestions(),

              ElevatedButton(
                style: ElevatedButton.styleFrom(
                  fixedSize: const Size.fromWidth(199),
                  elevation: 1,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(10),
                  ),
                ),
                onPressed: _generateStory,
                child: const Text(
                  "이야기 생성하기",
                  style: TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.w700,
                  ),
                ),
              ),
            ],
          );
        },
      ),
    );
  }
}
