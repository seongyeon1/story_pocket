import 'package:flutter/material.dart';

class ElderStoryScreen extends StatefulWidget {
  const ElderStoryScreen({super.key});

  @override
  State<ElderStoryScreen> createState() => _ElderStoryScreenState();
}

class _ElderStoryScreenState extends State<ElderStoryScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        actions: [
          IconButton(
            onPressed: () {},
            icon: const Icon(Icons.monetization_on_rounded),
          ),
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
      body: const Text("asds"),
    );
  }
}
