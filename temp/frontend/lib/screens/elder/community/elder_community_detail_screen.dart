import 'package:flutter/material.dart';
import 'package:my_project/models/story.dart';

class ElderCommunityDetailScreen extends StatelessWidget {
  final Story story;
  const ElderCommunityDetailScreen({super.key, required this.story});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(story.title),
      ),
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text("제목 : ${story.title}"),
          ],
        ),
      ),
    );
  }
}
