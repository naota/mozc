# Copyright 2010-2012, Google Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#     * Neither the name of Google Inc. nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# rewriter_base.gyp defines targets for lower layers to link to the rewriter
# modules, so modules in lower layers do not depend on ones in higher layers,
# avoiding circular dependencies.
{
  'variables': {
    'relative_dir': 'rewriter',
    'gen_out_dir': '<(SHARED_INTERMEDIATE_DIR)/<(relative_dir)',
  },
  'targets': [
    {
      'target_name': 'gen_rewriter_files',
      'type': 'none',
      'dependencies': [
        '../dictionary/dictionary_base.gyp:pos_util',
      ],
      'toolsets': ['host'],
      'actions': [
        {
          'action_name': 'gen_collocation_data',
          'variables': {
            'input_files%': [
              '../data/dictionary/collocation.txt',
            ],
          },
          'inputs': [
            '<@(input_files)',
          ],
          'conditions': [
          ],
          'outputs': [
            '<(gen_out_dir)/embedded_collocation_data.h',
          ],
          'action': [
            'python', '../build_tools/redirect.py',
            '<(gen_out_dir)/embedded_collocation_data.h',
            '<(mozc_build_tools_dir)/gen_collocation_data_main',
            '--collocation_data=<@(input_files)',
          ],
        },
        {
          'action_name': 'gen_collocation_suppression_data',
          'variables': {
            'input_files%': [
              '../data/dictionary/collocation_suppression.txt',
            ],
          },
          'inputs': [
            '<@(input_files)',
          ],
          'conditions': [
          ],
          'outputs': [
            '<(gen_out_dir)/embedded_collocation_suppression_data.h',
          ],
          'action': [
            'python', '../build_tools/redirect.py',
            '<(gen_out_dir)/embedded_collocation_suppression_data.h',
            '<(mozc_build_tools_dir)/gen_collocation_suppression_data_main',
            '--suppression_data=<@(input_files)',
          ],
        },
        {
          'action_name': 'gen_single_kanji_rewriter_data',
          'variables': {
            'input_file': '../data/single_kanji/single_kanji.tsv',
            'id_def': '../data/dictionary/id.def',
            'special_pos': '../data/rules/special_pos.def',
            'user_pos': '../data/rules/user_pos.def',
            'cforms': '../data/rules/cforms.def',
            'output_file': '<(gen_out_dir)/single_kanji_rewriter_data.h',
          },
          'inputs': [
            'embedded_dictionary_compiler.py',
            'gen_single_kanji_rewriter_data.py',
            '<(input_file)',
            '<(id_def)',
            '<(special_pos)',
            '<(user_pos)',
            '<(cforms)',
          ],
          'outputs': [
            '<(output_file)'
          ],
          'action': [
            'python', 'gen_single_kanji_rewriter_data.py',
            '--input=<(input_file)',
            '--min_prob=0.0',
            '--id_file=<(id_def)',
            '--special_pos_file=<(special_pos)',
            '--user_pos_file=<(user_pos)',
            '--cforms_file=<(cforms)',
            '--output=<(output_file)',
          ],
        },
        {
          'action_name': 'gen_symbol_rewriter_data',
          'variables': {
            'input_files': [
              '../data/symbol/symbol.tsv',
              '../data/rules/sorting_map.tsv',
              '../data/symbol/ordering_rule.txt',
            ],
          },
          'inputs': [
            '<@(input_files)',
          ],
          'outputs': [
            '<(gen_out_dir)/symbol_rewriter_data.h',
          ],
          'action': [
            '<(mozc_build_tools_dir)/gen_symbol_rewriter_dictionary_main',
            '<@(input_files)',
            '--logtostderr',
            '--output=<(gen_out_dir)/symbol_rewriter_data.h',
          ],
        },
        {
          'action_name': 'gen_emoticon_rewriter_data',
          'variables': {
            'input_file': '../data/emoticon/emoticon.tsv',
            'output_file': '<(gen_out_dir)/emoticon_rewriter_data.h',
          },
          'inputs': [
            'embedded_dictionary_compiler.py',
            'gen_emoticon_rewriter_data.py',
            '<(input_file)',
          ],
          'outputs': [
            '<(output_file)'
          ],
          'action': [
            'python', 'gen_emoticon_rewriter_data.py',
            '--input=<(input_file)',
            '--output=<(output_file)',
          ],
        },
        {
          'action_name': 'gen_reading_correction_data',
          'variables': {
            'input_files%': [
              '../data/dictionary/reading_correction.tsv',
            ],
          },
          'inputs': [
            '<@(input_files)',
          ],
          'conditions': [
          ],
          'outputs': [
            '<(gen_out_dir)/reading_correction_data.h',
          ],
          'action': [
            'python', './gen_reading_correction_data.py',
            '--output=<(gen_out_dir)/reading_correction_data.h',
            '--input=<@(input_files)',
          ],
        },
      ],
      'conditions': [
        ['target_platform!="Android"', {
          'actions': [
            {
              'action_name': 'gen_usage_rewriter_data',
              'variables': {
                'usage_data_file': [
                  '<(DEPTH)/third_party/japanese_usage_dictionary/usage_dict.txt',
                ],
                'cforms_file': [
                  '../data/rules/cforms.def',
                ],
              },
              'inputs': [
                '<@(usage_data_file)',
                '<@(cforms_file)',
              ],
              'outputs': [
                '<(gen_out_dir)/usage_rewriter_data.h',
              ],
              'action': [
                '<(mozc_build_tools_dir)/gen_usage_rewriter_dictionary_main',
                '--usage_data_file=<@(usage_data_file)',
                '--cforms_file=<@(cforms_file)',
                '--logtostderr',
                '--output=<(gen_out_dir)/usage_rewriter_data.h',
              ],
            },
          ],
        }],
      ],
    },
    {
      'target_name': 'gen_collocation_data_main',
      'type': 'executable',
      'toolsets': ['host'],
      'sources': [
        'gen_collocation_data_main.cc',
        'gen_existence_header.cc'
      ],
      'dependencies': [
        '../storage/storage.gyp:storage',
      ],
    },
    {
      'target_name': 'install_gen_collocation_data_main',
      'type': 'none',
      'toolsets': ['host'],
      'variables': {
        'bin_name': 'gen_collocation_data_main'
      },
      'includes' : [
        '../gyp/install_build_tool.gypi',
      ]
    },
    {
      'target_name': 'gen_collocation_suppression_data_main',
      'type': 'executable',
      'toolsets': ['host'],
      'sources': [
        'gen_collocation_suppression_data_main.cc',
        'gen_existence_header.cc'
      ],
      'dependencies': [
        '../storage/storage.gyp:storage',
      ],
    },
    {
      'target_name': 'install_gen_collocation_suppression_data_main',
      'type': 'none',
      'toolsets': ['host'],
      'variables': {
        'bin_name': 'gen_collocation_suppression_data_main'
      },
      'includes' : [
        '../gyp/install_build_tool.gypi',
      ]
    },
    {
      'target_name': 'gen_symbol_rewriter_dictionary_main',
      'type': 'executable',
      'toolsets': ['host'],
      'sources': [
        'dictionary_generator.cc',
        'embedded_dictionary.cc',
        'gen_symbol_rewriter_dictionary_main.cc',
      ],
      'dependencies': [
        '../base/base.gyp:base',
        '../data_manager/data_manager.gyp:user_pos_manager',
        '../dictionary/dictionary_base.gyp:pos_matcher',
        '../dictionary/dictionary_base.gyp:user_pos_data',
      ],
    },
    {
      'target_name': 'install_gen_symbol_rewriter_dictionary_main',
      'type': 'none',
      'toolsets': ['host'],
      'variables': {
        'bin_name': 'gen_symbol_rewriter_dictionary_main'
      },
      'includes' : [
        '../gyp/install_build_tool.gypi',
      ]
    },
    {
      'target_name': 'gen_usage_rewriter_dictionary_main',
      'type': 'executable',
      'toolsets': ['host'],
      'sources': [
        'gen_usage_rewriter_dictionary_main.cc',
      ],
      'dependencies': [
        '../base/base.gyp:base',
      ],
    },
    {
      'target_name': 'install_gen_usage_rewriter_dictionary_main',
      'type': 'none',
      'toolsets': ['host'],
      'variables': {
        'bin_name': 'gen_usage_rewriter_dictionary_main'
      },
      'includes' : [
        '../gyp/install_build_tool.gypi',
      ]
    },
  ],
}