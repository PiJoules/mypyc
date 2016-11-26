# -*- coding: utf-8 -*-

import cgen


class Value(cgen.Value):
    def get_decl_pair(self):
        return [str(self.typename)], self.name

