#ifndef LIB_H
#define LIB_H

#include <QString>

QString readFile(QString filename) noexcept; // Add noexcept specifier for exception safety
{
    QFile file(filename);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text)) {
        QString errorMsg = "Failed to open file for reading: " + file.errorString();
        throw std::runtime_error(errorMsg.toStdString());
    }
    QTextStream in(&file);
    QString text = in.readAll();
    file.close();
    return text;
}

#endif // LIB_H
