import 'package:flutter/material.dart';
import 'package:my_project/models/story.dart';

class ElderContentsDetailScreen extends StatelessWidget {
  final Story story;
  const ElderContentsDetailScreen({super.key, required this.story});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(story.title),
      ),
    );
  }
}
