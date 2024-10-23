import 'package:flutter/material.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter STT Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: SpeechToTextDemo(),
    );
  }
}

class SpeechToTextDemo extends StatefulWidget {
  @override
  _SpeechToTextDemoState createState() => _SpeechToTextDemoState();
}

class _SpeechToTextDemoState extends State<SpeechToTextDemo> {
  stt.SpeechToText? _speech; // nullable로 변경
  bool _isListening = false;
  String _text = '';

  @override
  void initState() {
    super.initState();
    _speech = stt.SpeechToText(); // 초기화
  }

  void _listen() async {
    if (_isListening) {
      await _speech!.stop(); // null 체크 후 호출
    } else {
      await _speech!.initialize(); // null 체크 후 호출
      await _speech!.listen(onResult: (result) {
        setState(() {
          _text = result.recognizedWords;
        });
      });
    }
    setState(() {
      _isListening = !_isListening;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Speech to Text Demo'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              _text,
              style: TextStyle(fontSize: 24),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: _listen,
              child: Text(_isListening ? 'Stop Listening' : 'Start Listening'),
            ),
          ],
        ),
      ),
    );
  }
}
