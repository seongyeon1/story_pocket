import 'package:flutter/material.dart';

class ElderPointScreen extends StatefulWidget {
  const ElderPointScreen({super.key});

  @override
  State<ElderPointScreen> createState() => _ElderPointScreenState();
}

class _ElderPointScreenState extends State<ElderPointScreen> {
  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: Text("포인트 확인 화면"),
    );
  }
}
