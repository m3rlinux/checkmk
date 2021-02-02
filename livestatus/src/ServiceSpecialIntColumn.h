// Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
// This file is part of Checkmk (https://checkmk.com). It is subject to the
// terms and conditions defined in the file COPYING, which is part of this
// source code package.

#ifndef ServiceSpecialIntColumn_h
#define ServiceSpecialIntColumn_h

#include "config.h"  // IWYU pragma: keep

#include <cstdint>
#include <string>

#include "IntColumn.h"
#include "contact_fwd.h"
class ColumnOffsets;
class Row;

class ServiceSpecialIntColumn : public IntColumn {
public:
    enum class Type { real_hard_state };

    ServiceSpecialIntColumn(const std::string &name,
                            const std::string &description,
                            const ColumnOffsets &offsets, Type ssic_type)
        : IntColumn(name, description, offsets), _type(ssic_type) {}

    int32_t getValue(Row row, const contact *auth_user) const override;

private:
    const Type _type;
};

#endif  // ServiceSpecialIntColumn_h
