import 'package:flutter/material.dart';
import 'package:my_project/models/story.dart';

class ElderStoryDetailScreen extends StatelessWidget {
  final Story story;
  const ElderStoryDetailScreen({super.key, required this.story});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(story.title),
      ),
    );
  }
}
