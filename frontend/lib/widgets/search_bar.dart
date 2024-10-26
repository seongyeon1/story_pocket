import 'package:flutter/material.dart';

class SearchBarForStories extends StatelessWidget {
  final List<Widget> trailing;
  final WidgetStateProperty<double>? elevation;
  final BoxConstraints? constraints;
  final String? hintText;

  const SearchBarForStories({
    super.key,
    this.trailing = const [],
    this.elevation = const WidgetStatePropertyAll(1),
    this.constraints = const BoxConstraints(maxHeight: 50, maxWidth: 350),
    this.hintText = "검색어를 입력하세요.",
  });

  @override
  Widget build(BuildContext context) {
    return SearchBar(
      trailing: trailing,
      elevation: elevation,
      constraints: constraints,
      hintText: hintText,
    );
  }
}
